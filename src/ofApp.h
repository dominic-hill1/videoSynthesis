#pragma once

#include "ofMain.h"
//#include "ofxOMXVideoGrabber.h"

class ofApp : public ofBaseApp{
	
public:

	void setup();
	void update();
	void draw();
	void exit();
	
	void keyPressed(int key);
	void keyReleased(int key);
	
	
	ofShader shader1;
	
    ofFbo framebuffer0;
    ofFbo framebuffer1;
    
    //ofFbo aspectFixFb;
    
    ofVideoGrabber input1;
	ofVideoPlayer movie1;

	ofSerial serial;
	string receivedData;
	int nano;
    
    void allocateAndDeclareSundries();
	void inputSetup();
	void inputUpdate();

	void audioIn(ofSoundBuffer & input);

	vector <float> left;
	vector <float> right;
	vector <float> volHistory;
	
	int 	bufferCounter;
	int 	drawCounter;
	
	float smoothedVol;
	float scaledVol;
	
	ofSoundStream soundStream;
    
    /*
    void omx_settings();
	void omx_updates();
	ofxOMXCameraSettings settings;
    ofxOMXVideoGrabber videoGrabber;
    */
    
    
};
