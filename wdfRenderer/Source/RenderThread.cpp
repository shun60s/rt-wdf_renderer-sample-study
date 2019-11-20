/*
  ==============================================================================

    RenderThread.cpp
    Created: 2 May 2016 12:45:29pm
    Author:  Maximilian Rest

  ==============================================================================
*/

/*
===============================================================================
Change: 
  output file name for windows, disable CSV output and etc , July-2019, Shun
  output file name is  append -output-rtwdf to input file name, November-2019, Shun
  delete Resampler fucntion, November-2019, Shun
  stereo input available,    November-2019, Shun
  wdf compute parallel by openmp, November-2019, Shun

===============================================================================
*/

#include <omp.h> 
#include "RenderThread.h"


RenderThread::RenderThread() : ThreadWithProgressWindow ("Processing Audio file through WDF", true, true)
{
}

void RenderThread::run( )
{

    const int blockSize = myRenderParams->blockSize;
    const int numBlocks = int(ceil( myRenderParams->transportSource->getTotalLength() / blockSize ));

    myRenderParams->totalBlocks = numBlocks;

   AudioSampleBuffer buf(myRenderParams->numChannels, blockSize);  // 32bit float  AudioBuffer (int numChannelsToAllocate, int numSamplesToAllocate)
   
   AudioSourceChannelInfo myACHI(buf);

 



    WavAudioFormat wav;

    File myFile (myRenderParams->inFile + "-output-rtwdf.wav");  // change output file name for windows 10
    TemporaryFile tempFile(myFile);
    ScopedPointer <OutputStream> outStream (tempFile.getFile().createOutputStream());

    if (outStream != nullptr)
    {

		 ScopedPointer <AudioFormatWriter> writer(wav.createWriterFor(outStream, myRenderParams->outputSampleRate, myRenderParams->numChannels, myRenderParams->outputBitDepth, NULL, 0));
  
		if (writer != nullptr)
        {
            outStream.release();
            float outVoltage[1];
            float outVoltage2[1];

            myRenderParams->transportSource->setPosition(0);
            myRenderParams->transportSource->start();
            myRenderParams->renderTime = 0;
            myRenderParams->badBlocks = 0;
            double blockTime =  (double)myRenderParams->blockSize / myRenderParams->inputSampleRate;

            for ( int n = 0; n <= numBlocks; n++)
            {
                if (threadShouldExit())
                {
                    myRenderParams->transportSource->stop();

                    outStream = nullptr;
                    tempFile.deleteTemporaryFile();
                    writer = nullptr;

                    return;
                }

                myRenderParams->transportSource->getNextAudioBlock( myACHI );

                double currentTime =  Time::getCurrentTime().toMilliseconds();


             
             
                for (int sample = 0; sample < myACHI.numSamples; sample++)
                {
                    myRenderParams->upBuf[sample] = myACHI.buffer->getSample(0, sample);
                   if( myRenderParams->numChannels ==2) {
                    myRenderParams->upBuf2[sample] = myACHI.buffer->getSample(1, sample);
                    }
                }

// openmp:  need openMP support Yes, /openmp flag
				omp_set_num_threads(2);    // Due to stereo process, thread number is 2.
#pragma omp parallel sections
//#pragma omp parallel
{
	
#pragma omp section
   {
                for (int sample = 0; sample < myACHI.numSamples; sample++)
                {
                    myRenderParams->myWdfTree->setInputValue(myRenderParams->upBuf[sample]  );
                    myRenderParams->myWdfTree->cycleWave();
                    myRenderParams->downBuf[sample] = { (float)(myRenderParams->myWdfTree->getOutputValue()) };
                    
                }
   }
#pragma omp section
   {
                for (int sample2 = 0; sample2 < myACHI.numSamples; sample2++)
                {
                    if( myRenderParams->numChannels ==2){
                    myRenderParams->myWdfTree2->setInputValue(myRenderParams->upBuf2[sample2] );
                    myRenderParams->myWdfTree2->cycleWave();
                    myRenderParams->downBuf2[sample2] = { (float)(myRenderParams->myWdfTree2->getOutputValue()) };
                    }
                    else myRenderParams->downBuf2[sample2]=0.0;

                }
   }
}
   
   
                double blockRenderTime = (Time::getCurrentTime().toMilliseconds() - currentTime)/(double)1000.0;
                myRenderParams->renderTime += blockRenderTime;
                if (blockRenderTime > blockTime)
                {
                    myRenderParams->badBlocks++;
                }


/*
                for (int sample = 0; sample < myACHI.numSamples; sample++)
                {
                    outVoltage[0] = { (myRenderParams->downBuf[sample])};
                     outVoltage2[0] = { (myRenderParams->downBuf2[sample]) };
                     //  outVoltage[0] = { (float)myRenderParams->downBuf[sample] };
                     //  outVoltage2[0] = { (float)myRenderParams->downBuf2[sample] };
                    // outVoltage[0] = { (float)myACHI.buffer->getSample(0, sample) };   // this is 1kHz ok
                    // outVoltage2[0] = { (float)myACHI.buffer->getSample(1, sample) };  // this is 500Hz OK
                    float const *const tmp[] = { outVoltage, outVoltage2,0 };
                    writer->writeFromFloatArrays( tmp, myRenderParams->numChannels, 1);
           
				}

*/
                // write a block data at once
				float const *const tmp[] = { myRenderParams->downBuf ,myRenderParams->downBuf2 ,0 };
				writer->writeFromFloatArrays(tmp, myRenderParams->numChannels, myACHI.numSamples);



#define DISP_COUNT 20
                if ( (n % DISP_COUNT) == 0)
                {
                    setProgress ( n / (double)numBlocks );
                 }
            }

            myRenderParams->transportSource->stop();


        }
        writer = nullptr;
        outStream = nullptr;
        tempFile.overwriteTargetFileWithTemporary();

    }


}

void RenderThread::setRenderParamsPtr( RenderParams* myRenderParams )
{
    this->myRenderParams = myRenderParams;
}
