#include "ofApp.h"

#include "iostream"

#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>

#define MIDI_MAGIC 63.50f
#define CONTROL_THRESHOLD .04f

// float az = 0;
// float sx = 0;
// float dc = 0;
// float fv = 0;
// float jm = 0;
// float hn = 0;


float eddebeeabdaabf = 0;float eaccbacad = 0;float cadfeacfebeabfe = 0;float bdbbadbffefbb = 0;float cabdefbeed = 0;float bdbbbaeccbddd = 0;float fcdbfdcbb = 0;float adaacfcdadbee = 0;float fdfdfbbfbcbac = 0;float eafbaedef = 0;float ebeaeffffeecb = 0;float bfdbdaacbbebe = 0;

int width=0;
int height=0;

const int controlSize=17;

float control1[controlSize];

bool midiActiveFloat[controlSize];

float time1 = 0.0;
float time2 = 0.0;
float rate = 0.01;

//--------------------------------------------------------------
void ofApp::setup() {
	ofSetVerticalSync(true);
	ofSetFrameRate(30);
    ofBackground(0);
    ofHideCursor();
	
	width=640;
	height=480;
	
	inputSetup();
	bool loaded = movie1.load("space.mp4");
    if (!loaded) {
        ofLogError() << "Failed to load video file!";
        return;
    } 
	movie1.play();
	movie1.setVolume(0);

	allocateAndDeclareSundries();
	
	shader1.load("shadersES2/shader1");

	// serial.setup("/dev/ttyACM0", 9600);
	

	// Audio Setup
	soundStream.printDeviceList();
	
	int bufferSize = 256;

	left.assign(bufferSize, 0.0);
	right.assign(bufferSize, 0.0);
	volHistory.assign(400, 0.0);
	
	bufferCounter	= 0;
	drawCounter		= 0;
	smoothedVol     = 0.0;
	scaledVol		= 0.0;


	ofSoundStreamSettings settings;
	auto devices = soundStream.getMatchingDevices("default");
	if(!devices.empty()){
		settings.setInDevice(devices[0]);
	}

	settings.setInListener(this);
	settings.sampleRate = 44100;
	#ifdef TARGET_EMSCRIPTEN
		settings.numOutputChannels = 2;
	#else
		settings.numOutputChannels = 0;
	#endif
	settings.numInputChannels = 1;
	settings.bufferSize = bufferSize;
	soundStream.setup(settings);



}
//--------------------------------------------------------------
void ofApp::inputSetup(){

	input1.setDesiredFrameRate(30);
	input1.initGrabber(width,height);
}
//------------------------------------------------------------
void ofApp::allocateAndDeclareSundries(){
	framebuffer0.allocate(width,height);
	framebuffer0.begin();
	ofClear(0,0,0,255);
	framebuffer0.end();

	framebuffer1.allocate(width, height);
	framebuffer1.begin();
	ofClear(0, 0, 0, 255);
	framebuffer1.end();

}
//--------------------------------------------------------------
void ofApp::update() {
	input1.update();
	// movie1.update();

	using namespace boost::interprocess;

    // Open the shared memory object created by Python
    shared_memory_object shm(open_only, "psm_18157efa", read_only);  // Replace with the actual name printed by the Python script

    // Map the whole shared memory in this process
    mapped_region region(shm, read_only);

    // Read data from the shared memory
    char* receivedData = static_cast<char*>(region.get_address());

	std::string reload = "RELOAD";
	std::string str;
    str = receivedData;  // Assign char* to std::string

    std::cout << "Read from shared memory: " << receivedData << std::endl;
	if (str.substr(0, 6) == reload){
		 std::cout << "RELOADING" << std::endl;
		 shader1.load("shadersES2/shader1");
		 shader1.setUniform1f("eddebeeabdaabf", eddebeeabdaabf);
std::cout << eddebeeabdaabf << std::endl;shader1.setUniform1f("eaccbacad", eaccbacad);
std::cout << eaccbacad << std::endl;shader1.setUniform1f("cadfeacfebeabfe", cadfeacfebeabfe);
std::cout << cadfeacfebeabfe << std::endl;shader1.setUniform1f("bdbbadbffefbb", bdbbadbffefbb);
std::cout << bdbbadbffefbb << std::endl;shader1.setUniform1f("cabdefbeed", cabdefbeed);
std::cout << cabdefbeed << std::endl;shader1.setUniform1f("bdbbbaeccbddd", bdbbbaeccbddd);
std::cout << bdbbbaeccbddd << std::endl;shader1.setUniform1f("fcdbfdcbb", fcdbfdcbb);
std::cout << fcdbfdcbb << std::endl;shader1.setUniform1f("adaacfcdadbee", adaacfcdadbee);
std::cout << adaacfcdadbee << std::endl;shader1.setUniform1f("fdfdfbbfbcbac", fdfdfbbfbcbac);
std::cout << fdfdfbbfbcbac << std::endl;shader1.setUniform1f("eafbaedef", eafbaedef);
std::cout << eafbaedef << std::endl;shader1.setUniform1f("ebeaeffffeecb", ebeaeffffeecb);
std::cout << ebeaeffffeecb << std::endl;shader1.setUniform1f("bfdbdaacbbebe", bfdbdaacbbebe);
std::cout << bfdbdaacbbebe << std::endl;
	}else{
		std::istringstream stream(receivedData);
		std::string varName;
		std::string value;
		float varValue;
		stream >> varName;
		stream >> value;
		try{
			varValue = std::stof(value);
		} catch (const std::invalid_argument& e) {
			std::cerr << "Invalid argument: " << e.what() << std::endl;
		} catch (const std::out_of_range& e) {
			std::cerr << "Out of range: " << e.what() << std::endl;
		}

		if (varName == "eddebeeabdaabf"){eddebeeabdaabf= varValue;}if (varName == "eaccbacad"){eaccbacad= varValue;}if (varName == "cadfeacfebeabfe"){cadfeacfebeabfe= varValue;}if (varName == "bdbbadbffefbb"){bdbbadbffefbb= varValue;}if (varName == "cabdefbeed"){cabdefbeed= varValue;}if (varName == "bdbbbaeccbddd"){bdbbbaeccbddd= varValue;}if (varName == "fcdbfdcbb"){fcdbfdcbb= varValue;}if (varName == "adaacfcdadbee"){adaacfcdadbee= varValue;}if (varName == "fdfdfbbfbcbac"){fdfdfbbfbcbac= varValue;}if (varName == "eafbaedef"){eafbaedef= varValue;}if (varName == "ebeaeffffeecb"){ebeaeffffeecb= varValue;}if (varName == "bfdbdaacbbebe"){bfdbdaacbbebe= varValue;}
	}

	// std::cout << "Read from shared memory: " << receivedData << std::endl;

	

	// while (serial.available() > 0) {
	// 	char byteData = serial.readByte();
	// 	if (byteData == '\n') { // Check for the end of the message
	// 		std::istringstream stream(receivedData);
	// 		std::string varName;
	// 		std::string varValue;
	// 		stream >> varName;
	// 		stream >> varValue

			
	// 		if (varName == fedaafbfbccbc){fedaafbfbccbc= varValue}if (varName == daaabffdbda){daaabffdbda= varValue}if (varName == dcbcad){dcbcad= varValue}
	


	// 		receivedData = ""; // Clear the string for new data
	// 	} else {
	// 		receivedData += byteData; // Append the byte to the string
	// 	}
	// }

	scaledVol = ofMap(smoothedVol, 0.0, 0.17, 0.0, 1.0, true);

	volHistory.push_back( scaledVol );
	
	if( volHistory.size() >= 400 ){
		volHistory.erase(volHistory.begin(), volHistory.begin()+1);
	}
}
//--------------------------------------------------------------
void ofApp::draw() {

	time1 += 1;
	// time2 += 0.5;

	framebuffer0.begin();
	shader1.begin();
	// input1.draw(0,0);
	framebuffer1.draw(0, 0);

	shader1.setUniformTexture("input1", input1.getTexture(), 1); // "1" must be incremented with multiple inputs
	// shader1.setUniformTexture("input1", movie1.getTexture(), 1); // "1" must be incremented with multiple inputs
	// movie1.draw(0, 0, 400, 300);
	// az = nano/100;
	shader1.setUniform2f("resolution", 720, 480);
	shader1.setUniform1f("time", time1);

	shader1.setUniform1f("eddebeeabdaabf", eddebeeabdaabf);
std::cout << eddebeeabdaabf << std::endl;shader1.setUniform1f("eaccbacad", eaccbacad);
std::cout << eaccbacad << std::endl;shader1.setUniform1f("cadfeacfebeabfe", cadfeacfebeabfe);
std::cout << cadfeacfebeabfe << std::endl;shader1.setUniform1f("bdbbadbffefbb", bdbbadbffefbb);
std::cout << bdbbadbffefbb << std::endl;shader1.setUniform1f("cabdefbeed", cabdefbeed);
std::cout << cabdefbeed << std::endl;shader1.setUniform1f("bdbbbaeccbddd", bdbbbaeccbddd);
std::cout << bdbbbaeccbddd << std::endl;shader1.setUniform1f("fcdbfdcbb", fcdbfdcbb);
std::cout << fcdbfdcbb << std::endl;shader1.setUniform1f("adaacfcdadbee", adaacfcdadbee);
std::cout << adaacfcdadbee << std::endl;shader1.setUniform1f("fdfdfbbfbcbac", fdfdfbbfbcbac);
std::cout << fdfdfbbfbcbac << std::endl;shader1.setUniform1f("eafbaedef", eafbaedef);
std::cout << eafbaedef << std::endl;shader1.setUniform1f("ebeaeffffeecb", ebeaeffffeecb);
std::cout << ebeaeffffeecb << std::endl;shader1.setUniform1f("bfdbdaacbbebe", bfdbdaacbbebe);
std::cout << bfdbdaacbbebe << std::endl;




	// shader1.setUniform1f("sx",sx* 10);
	// shader1.setUniform1f("az",az * 10);
	// shader1.setUniform1f("fv",fv * 10);
	// // shader1.setUniform1f("audio", scaledVol);
	// shader1.setUniform1f("audio", 0);
	// shader1.setUniform1f("time1",time1);
	// shader1.setUniform1f("time2", time2);
	// // shader1.setUniform1f("nano1", nano);
	// shader1.setUniform1f("nano1", az * 10);



	shader1.end();


	// ofSetColor(127 + 127 * sin(time1), 200, 127 - 127 * sin(time2), 255);
	// // ofDrawEllipse(mouseX, mouseY, 20+80*abs(sin(time1)), 20+80*abs(sin(time2)));
	// ofDrawEllipse(720/2, 480/2, 20+80*abs(sin(time1)), 20+80*abs(sin(time2)));
	// ofSetColor(0);
	// ofDrawEllipse(720/2, 480/2, 18+80*abs(sin(time1)), 18+80*abs(sin(time2)));
	// // ofDrawEllipse(mouseX, mouseY, 18+80*abs(sin(time1)), 18+80*abs(sin(time2)));


	framebuffer0.end();
	
	framebuffer0.draw(0,0,720,480);

	framebuffer1.begin();
	framebuffer0.draw(0, 0);
	framebuffer1.end();

	// movie1.draw(0, 480);
	

    ofSetColor(255);
    // string msg="fps="+ofToString(ofGetFrameRate(),2)+" sx = " +ofToString(sx,2)+" time = " +ofToString(time1,2) + " audio = " +ofToString(scaledVol,2) +  " az = " +ofToString(az,2) + " fv = " +ofToString(fv,2);
    // ofDrawBitmapString(msg,10,10);
}

//--------------------------------------------------------------
void ofApp::exit() {

}

void ofApp::audioIn(ofSoundBuffer & input){
	
	float curVol = 0.0;
	
	// samples are "interleaved"
	int numCounted = 0;	

	//lets go through each sample and calculate the root mean square which is a rough way to calculate volume	
	for (size_t i = 0; i < input.getNumFrames(); i++){
		left[i]		= input[i*2]*0.5;
		right[i]	= input[i*2+1]*0.5;

		curVol += left[i] * left[i];
		curVol += right[i] * right[i];
		numCounted+=2;
	}
	
	//this is how we get the mean of rms :)
	curVol /= (float)numCounted;
	
	// this is how we get the root of rms :)
	curVol = sqrt( curVol );
	
	smoothedVol *= 0.93;
	smoothedVol += 0.07 * curVol;
	
	bufferCounter++;
	
}


//--------------------------------------------------------------
void ofApp::keyPressed(int key) {
	
// 	//here is how i map controls from the keyboard
    
//     //increment and decrement sx
//     if (key == 's') {sx += .01;}
//     if (key == 'x') {sx -= .01;}
    
//     //increment and decrement dc
//     if (key == 'd') {dc += .01;}
//     if (key == 'c') {dc -= .01;}

// 	if (key == 'a') {az += .01;}
//     if (key == 'z') {az -= .01;}

// 	if (key == 'f') {fv += .01;}
//     if (key == 'v') {fv -= .01;}

// 	if (key == 'j') {jm += .01;}
//     if (key == 'm') {jm -= .01;}

// 	if (key == 'h') {hn += .01;}
//     if (key == 'n') {hn -= .01;}
        
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key) {
	
}

