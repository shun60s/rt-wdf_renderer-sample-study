/*
 ==============================================================================

 This file was auto-generated!

 ==============================================================================
 */
 /*
===============================================================================
Change: 
  build for vs2017, disable downsample and etc , July-2019, Shun
  add two triode amp, September, Shun 
  add triode sadou push-pull amp, October-2019, Shun
  add wdfSadouPushPushVCVSConnectionTriodeAmpTree2, October-2019, Shun
  delete Resampler fucntion, November-2019, Shun
  stereo input available,    November-2019, Shun
  layout size change,        November-2019, Shun
  
===============================================================================
*/
 

#ifndef MAINCOMPONENT_H_INCLUDED
#define MAINCOMPONENT_H_INCLUDED


#include <array>

#include "../JuceLibraryCode/JuceHeader.h"
#include "RenderThread.h"

using namespace juce;


// Circuits
#include "../../Circuits/wdfCCTAx1Tree.hpp"
#include "../../Circuits/wdfCCTAx4Tree.hpp"
#include "../../Circuits/wdfJTM45Tree.hpp"
#include "../../Circuits/wdfSwitchTree.hpp"
#include "../../Circuits/wdfTonestackTree.hpp"

#include "../../Circuits/wdfTwoTriodeAmpTree.hpp"
#include "../../Circuits/wdfSadouPushPushTriodeAmpTree.hpp"
#include "../../Circuits/wdfSadouPushPushVCVSConnectionTriodeAmpTree.hpp"
#include "../../Circuits/wdfSadouPushPushVCVSConnectionTriodeAmpTree2.hpp"


//==============================================================================
/*
 This component lives inside our window, and this is where you should put all
 your controls and content.
 */
class MainContentComponent   :  public Component,
                                public AudioIODeviceCallback,
                                public ChangeListener,
                                public Button::Listener,
                                public Slider::Listener,
                                public ComboBox::Listener
{
public:
    //==============================================================================
    MainContentComponent() {

        myLookAndFeel.setUsingNativeAlertWindows(true);
        LookAndFeel::setDefaultLookAndFeel(&myLookAndFeel);
        getLookAndFeel().setDefaultSansSerifTypefaceName("Arial");

        startupTime = Time::getCurrentTime().toMilliseconds();

        cout.precision(15);
        cout.setf(ios::fixed, ios::floatfield);
        cout.width(20);
        cout.fill(' ');

        addAndMakeVisible(groupParams);
        addAndMakeVisible(groupLogger);

        addAndMakeVisible (Logger = new TextEditor ("new text editor"));
        Logger->setMultiLine (true);
        Logger->setReturnKeyStartsNewLine (false);
        Logger->setReadOnly (true);
        Logger->setScrollbarsShown (true);
        Logger->setCaretVisible (true);
        Logger->setPopupMenuEnabled (true);
        Logger->setText (String::empty);
        
        addAndMakeVisible (&wdfTreeSelector);
        
        wdfTreeSelector.addItem("Tone Stack 44100Hz",1);
        wdfTreeSelector.addItem("CCTAx1 44100Hz",2);
        wdfTreeSelector.addItem("CCTAx4 176400Hz",3);
        wdfTreeSelector.addItem("JTM45 176400Hz",4);
        wdfTreeSelector.addItem("Switch 44100Hz",5);
        wdfTreeSelector.addItem("Two Triode Amp 44100Hz",6);
        wdfTreeSelector.addItem("Sadou PushPull Triode Amp 44100Hz",7);
        wdfTreeSelector.addItem("Sadou PushPull 44100Hz VCVSConnection Triode Amp",8);
#define SP8VTA 8
#define START_ID 8
        wdfTreeSelector.addItem("Sadou PushPull 88200Hz VCVSConnection Triode Amp", SP8VTA+1);
        wdfTreeSelector.setSelectedId(START_ID);

        wdfTreeSelector.addListener(this);
        
        addAndMakeVisible (&renderButton);
        renderButton.setButtonText ("Render");
        renderButton.addListener (this);
        renderButton.setEnabled (false);
        
        addAndMakeVisible (&openButton);
        openButton.setButtonText ("Open File");
        openButton.addListener (this);
        
        addAndMakeVisible (&bitDepthSelector);
        bitDepthSelector.addItem("16 bits",1);
        bitDepthSelector.setSelectedId(1);
        myRenderParams.outputBitDepth = 16;
        bitDepthSelector.addItem("24 bits",2);
        bitDepthSelector.addItem("32 bits",3);
        bitDepthSelector.addListener(this);
        
        wdfTreeArray[0].reset(new wdfTonestackTree());
        wdfTreeArray[1].reset(new wdfCCTAx1Tree());
        wdfTreeArray[2].reset(new wdfCCTAx4Tree());
        wdfTreeArray[3].reset(new wdfJTM45Tree());
        wdfTreeArray[4].reset(new wdfSwitchTree());

        wdfTreeArray2[0].reset(new wdfTonestackTree());
        wdfTreeArray2[1].reset(new wdfCCTAx1Tree());
        wdfTreeArray2[2].reset(new wdfCCTAx4Tree());
        wdfTreeArray2[3].reset(new wdfJTM45Tree());
        wdfTreeArray2[4].reset(new wdfSwitchTree());


        wdfTreeArray[5].reset(new wdfTwoTriodeAmpTree());
        wdfTreeArray[6].reset(new wdfSadouPushPullTriodeAmpTree());
        wdfTreeArray[7].reset(new wdfSadouPushPullVCVSconTriodeAmpTree());
        wdfTreeArray[8].reset(new wdfSadouPushPullVCVSconTriodeAmpTree2());
        
        wdfTreeArray2[5].reset(new wdfTwoTriodeAmpTree());
        wdfTreeArray2[6].reset(new wdfSadouPushPullTriodeAmpTree());
        wdfTreeArray2[7].reset(new wdfSadouPushPullVCVSconTriodeAmpTree());
        wdfTreeArray2[8].reset(new wdfSadouPushPullVCVSconTriodeAmpTree2());

        for(auto &wdfTree : wdfTreeArray){
            wdfTree->initTree();
        }
        
        
        for(auto &wdfTree : wdfTreeArray2){
            wdfTree->initTree();
        }
        

        UpdateWdfTree(START_ID-1);


        /*
        writeLogLine("Created WDF tree");
        groupParams.setText(myWdfTree->getTreeIdentifier());
        writeLogLine(String("wdfTree description: ") + String(myWdfTree->getTreeIdentifier()));
        */
        
        
        setSize (600, 460);
        writeLogLine("RT-WDF wav-file Renderer. Initializing..");

        formatManager.registerBasicFormats();
        transportSource.addChangeListener (this);

        // writeLogLine("Ready.");

		writeLogLine("Order: 1st select wdr, next open file, and last render");

    }

    
    void writeLogLine (String logLine) {
        String nowTime = String::formatted(("%08.3f"), (float)((int64)(Time::getCurrentTime().toMilliseconds()) - startupTime) / 1000.0f);
        Logger->insertTextAtCaret("\n"+nowTime+": "+logLine);
    }

    //=======================================================================
    void audioDeviceAboutToStart (AudioIODevice* device) override
    {
        // This function will be called when the audio device is started, or when
        // its settings (i.e. sample rate, block size, etc) are changed.

        // You can use this function to initialise any resources you might need,
        // but be careful - it will be called on the audio thread, not the GUI thread.

        // For more details, see the help for AudioProcessor::prepareToPlay()



    }
    //=======================================================================
    void audioDeviceStopped() override {

    }

    //=======================================================================
    void audioDeviceIOCallback (const float** inputChannelData, int numInputChannels,
                                float** outputChannelData, int numOutputChannels,
                                int numSamples) override {

    }


    //=======================================================================
    void paint (Graphics& g) override {
        // (Our component is opaque, so we must completely fill the background with a solid colour)
        g.fillAll (Colours::white);

        // You can add your drawing code here!
    }

    //=======================================================================
    void resized() override {
        // This is called when the MainContentComponent is resized.
        // If you add any child components, this is where you should
        // update their positions.

		juce::Rectangle<int> mainScreen = getLocalBounds().reduced(5);   // add juce:: for vc2017 ...

        // Parameter positioning
        juce::Rectangle<int> paramRect = mainScreen.removeFromTop(245);

        paramRect = paramRect.withTrimmedTop(20);
        groupParams.setBounds(paramRect);

        paramRect = paramRect.withTrimmedTop(40);

        size_t paramsPerCol = 5;
        juce::Rectangle<int> paramRowRect = paramRect.removeFromTop(60).reduced(5);


        int paramWidth = paramRect.getWidth()/paramsPerCol;
        size_t numParams = 0;
        for (auto& paramComp : paramComponents) {
            paramComp->setBounds(paramRowRect.removeFromLeft(paramWidth).reduced(8));
            numParams++;
            if ( (numParams % paramsPerCol) == 0 ) {
                paramRowRect = paramRect.removeFromTop(60).reduced(5);
            }

        }

        juce::Rectangle<int> fileButtons = mainScreen.removeFromTop(45);
        int buttonWidth = fileButtons.getWidth()/4;

        openButton.setBounds ( fileButtons.removeFromLeft(buttonWidth).reduced(8) );
        renderButton.setBounds ( fileButtons.removeFromLeft(buttonWidth).reduced(8) );
        bitDepthSelector.setBounds ( fileButtons.removeFromLeft(buttonWidth).reduced(8) );
        wdfTreeSelector.setBounds ( fileButtons.removeFromLeft(buttonWidth).reduced(8) );
        // Text box positioning
        groupLogger.setBounds(mainScreen);
        juce::Rectangle<int> textbox = mainScreen.withTrimmedTop(7).reduced(5);
        Logger->setBounds (textbox);
    }

    //=======================================================================
    void sliderValueChanged (Slider* slider) override {
        for (size_t i = 0; i < paramComponents.size(); i++) {
            if (slider == paramComponents[i].get()) {
                myWdfTree->setParam(i,slider->getValue());
				myWdfTree2->setParam(i, slider->getValue());
            }
        }
    }

    void comboBoxChanged(ComboBox* comboBoxThatHasChanged) override {
        if (comboBoxThatHasChanged == &bitDepthSelector) {
            int idChosen = comboBoxThatHasChanged->getSelectedId();
            if (idChosen == 1) {
                myRenderParams.outputBitDepth = 16;
            } else if (idChosen == 2) {
                myRenderParams.outputBitDepth = 24;
            } else if (idChosen == 3) {
                myRenderParams.outputBitDepth = 32;
            }
        }else if (comboBoxThatHasChanged == &wdfTreeSelector) {
            int idChosen = comboBoxThatHasChanged->getSelectedId();
            UpdateWdfTree(idChosen - 1);
        }
    }


    //=======================================================================
    void changeListenerCallback (ChangeBroadcaster* source) override {

    }

    //=======================================================================
    void buttonClicked (Button* button) override {
        if (button == &openButton) {
            openButtonClicked();
        }
        else if (button == &renderButton) {
            renderButtonClicked();
        }
        else {
            for (size_t i = 0; i < paramComponents.size(); i++) {
                if (button == paramComponents[i].get()) {
                    myWdfTree->setParam(i,button->getToggleState());
                }
            }
        }

    }



protected:
    //==============================================================================

    wdfTree* myWdfTree;
    wdfTree* myWdfTree2;
    std::array<std::unique_ptr<wdfTree>, SP8VTA+1> wdfTreeArray;
    std::array<std::unique_ptr<wdfTree>, SP8VTA+1> wdfTreeArray2;

    AudioDeviceManager myDeviceManager;

    GroupComponent groupParams;
    GroupComponent groupLogger;
    ScopedPointer<TextEditor> Logger;


	float* downBuf  = nullptr;
	float* downBuf2 = nullptr;
	float* upBuf    = nullptr;
	float* upBuf2   = nullptr;

    int64 startupTime;

    RenderParams myRenderParams;
    RenderThread myRenderer;

	AudioFormatReader* reader;


    void openButtonClicked() {
        FileChooser chooser ("Select a Wave file to play...",
                             File::nonexistent,
                             "*.wav");

        if (chooser.browseForFileToOpen()) {
            File file (chooser.getResult());
            inFile=file.getFileNameWithoutExtension();
            
            reader = formatManager.createReaderFor (file);

            if (reader) {
                double Fs = reader->sampleRate;
                myRenderParams.inputSampleRate = Fs;
                myRenderParams.outputSampleRate = Fs;
                transportSource.prepareToPlay (BLOCK_SIZE, Fs); //BS TODO

				myRenderParams.numChannels = reader->numChannels;
				writeLogLine("num Channel: "+String(myRenderParams.numChannels ));
				
				if ( reader->numChannels > 2) {
					writeLogLine("Error: please select mono or stereo wav file");
				}
                else if( Fs != myWdfTree->getSamplerate()){
                 	writeLogLine("Error: please select same Fs wav file as WdfTree, "+String(myWdfTree->getSamplerate())+"Hz");
                }
                else
                {
					writeLogLine("Base samplerate: " + String(Fs) + "Hz");
					renderButton.setEnabled (true);
                }
               
                ScopedPointer<AudioFormatReaderSource> newSource = new AudioFormatReaderSource (reader, true);
                transportSource.setSource (newSource, 0, nullptr, reader->sampleRate);
                
                myWdfTree->adaptTree( );
                myWdfTree2->adaptTree( );
      
                writeLogLine("'"+String(file.getFileName())+"' opened. Duration: "+String(transportSource.getLengthInSeconds())+"s");

                oversamplingRatio = myWdfTree->getSamplerate() / Fs;
                //writeLogLine("Base samplerate: "+String(Fs)+"Hz");
                //writeLogLine("wdfTree adapted for effective samplerate: "+String(myWdfTree->getSamplerate())+"Hz.");
                //writeLogLine("Resulting OX="+String(oversamplingRatio));
            
                myRenderParams.outputSampleRate = myWdfTree->getSamplerate();

                size_t downBufSize = ceil(oversamplingRatio * BLOCK_SIZE);

                if( downBuf)  delete[] downBuf;
                if( downBuf2) delete[] downBuf2;
                if( upBuf )   delete[] upBuf;
                if( upBuf2 )  delete[] upBuf2;
                	
                downBuf = new float[downBufSize]; //BS TODO
				downBuf2 = new float[downBufSize]; //BS TODO
                upBuf = new float[downBufSize]; //BS TODO
				upBuf2 = new float[downBufSize]; //BS TODO
               
                readerSource = newSource.release();
            }
        }
    }

    void renderButtonClicked() {
        myRenderParams.myWdfTree = myWdfTree;
        
        // Set nullptr if mono here
        if( myRenderParams.numChannels ==1)  myWdfTree2 = nullptr; 
        
        myRenderParams.myWdfTree2 = myWdfTree2;


		myRenderParams.transportSource = &transportSource;
		myRenderParams.downBuf = downBuf;
		myRenderParams.downBuf2 = downBuf2;
		myRenderParams.upBuf = upBuf;
		myRenderParams.upBuf2 = upBuf2;

        myRenderParams.blockSize = BLOCK_SIZE; //TODO
        myRenderParams.treeSampleRate = myWdfTree->getSamplerate();
        
        myRenderParams.inFile=inFile;
        
        renderButton.setEnabled (false);
         
        myRenderer.setRenderParamsPtr( &myRenderParams );
        writeLogLine("Rendering started");

        if( myRenderer.runThread(10) )
        {
            writeLogLine("Rendering finished");
            double audioTime = transportSource.getLengthInSeconds();
            writeLogLine("Audio Time: " + String(audioTime) + ". Rendering Time: " + String(myRenderParams.renderTime));
            writeLogLine("Realtimes needed: " + String((double)myRenderParams.renderTime/(double)audioTime));
            writeLogLine("Total Blocks: " + String((double)myRenderParams.totalBlocks) + ". Bad Blocks: " + String((double)myRenderParams.badBlocks));
        }
        else
        {
            writeLogLine("Rendering aborted");
        }
        // myLookAndFeel.playAlertSound();
    }

    void createParamControls(const std::vector<paramData>& paramsIn) {
        paramComponents.clear();
        paramLabels.clear();
        for (paramData param : paramsIn) {
            if (param.type == boolParam) {
                std::unique_ptr<ToggleButton> newButton(new ToggleButton());
                std::unique_ptr<Label> newLabel (new Label());
                newLabel->attachToComponent(newButton.get(), false);
                newLabel->setText(param.name, dontSendNotification);
                newButton->setButtonText(param.units);
                newButton->setToggleState(param.value, dontSendNotification);
                newButton->addListener (this);
                addAndMakeVisible (newButton.get());
                paramComponents.push_back(std::move(newButton));
                paramLabels.push_back(std::move(newLabel));
            }
            else if (param.type == doubleParam) {
                std::unique_ptr<Slider> newSlider(new Slider());
                std::unique_ptr<Label> newLabel (new Label());
                newLabel->attachToComponent(newSlider.get(), false);
                newLabel->setText(param.name, dontSendNotification);
                newSlider->setSliderStyle(Slider::RotaryVerticalDrag);
                newSlider->setRange(param.lowLim, param.highLim, 0.001 * (param.highLim - param.lowLim));
                newSlider->setValue(param.value);
                newSlider->setColour(Slider::ColourIds::rotarySliderFillColourId, Colours::black);
                newSlider->addListener (this);
                addAndMakeVisible (newSlider.get());
                paramComponents.push_back(std::move(newSlider));
                paramLabels.push_back(std::move(newLabel));
            }
        }
        resized();
    }

    
    void UpdateWdfTree(int inIndex)
    {     
        
        myWdfTree = wdfTreeArray[inIndex].get();
        myWdfTree2 = wdfTreeArray2[inIndex].get();
        myWdfTree->adaptTree( );
        myWdfTree2->adaptTree( );
        writeLogLine("Created two WDF tree");
        groupParams.setText(myWdfTree->getTreeIdentifier());
        writeLogLine(String("wdfTree description: ") + String(myWdfTree->getTreeIdentifier()));
        createParamControls(myWdfTree->getParams());
        
        
    }


    //==========================================================================
    TextButton openButton;
    TextButton renderButton;
    ComboBox wdfTreeSelector;
    ComboBox bitDepthSelector;
    std::vector<std::unique_ptr<Component> > paramComponents;
    std::vector<std::unique_ptr<Component> > paramLabels;
    double oversamplingRatio;
    String inFile;

    AudioFormatManager formatManager;
    ScopedPointer<AudioFormatReaderSource> readerSource;
    AudioTransportSource transportSource;

    LookAndFeel_V3 myLookAndFeel;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (MainContentComponent)
};


// (This function is called by the app startup code to create our main component)
Component* createMainContentComponent()     { return new MainContentComponent(); }


#endif  // MAINCOMPONENT_H_INCLUDED
