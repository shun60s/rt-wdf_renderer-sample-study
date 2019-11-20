/*
  ==============================================================================

    RenderThread.h
    Created: 2 May 2016 12:45:53pm
    Author:  Maximilian Rest

  ==============================================================================
  Change: 
      delete Resampler fucntion, November-2019, Shun
      stereo input available,    November-2019, Shun
  
*/

#ifndef RENDERTHREAD_H_INCLUDED
#define RENDERTHREAD_H_INCLUDED

#include "../JuceLibraryCode/JuceHeader.h"
#include "../../Libs/rt-wdf_lib/Libs/rt-wdf/rt-wdf.h"


#define TwoTriodeAmp 1
#define BLOCK_SIZE 512 //8192 //1024 //512


class RenderThread;
class RenderParams;


class RenderThread : public ThreadWithProgressWindow {
    
public:
    RenderThread( );
    void run( );
    void setRenderParamsPtr( RenderParams* myRenderParams );

    
private:
    RenderParams* myRenderParams;

};



class RenderParams {
    
public:
    wdfTree* myWdfTree;
    wdfTree* myWdfTree2;

    AudioTransportSource* transportSource;

	float* downBuf;
	float* downBuf2;
	float* upBuf;
	float* upBuf2;

    int blockSize;
    double outputSampleRate;
    double inputSampleRate;
    double treeSampleRate;
    double outputBitDepth;
    
    double renderTime;
    size_t badBlocks;
    size_t totalBlocks;
    
	int numChannels;
    String inFile;
};


#endif  // RENDERTHREAD_H_INCLUDED
