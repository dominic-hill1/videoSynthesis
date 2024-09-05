#include "ofApp.h"

#include "iostream"

#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>

#define MIDI_MAGIC 63.50f
#define CONTROL_THRESHOLD .04f


float caafbbbaa = 0;float efffdbfacedcdc = 0;float dcadeccabcbbaebef = 0;float fffaadfddd = 0;float fbcbdefbbda = 0;float dbececfedce = 0;float efbdeabbe = 0;float ffbabcefabaabfdcf = 0;float ddbdefaeaac = 0;float efaaaeefefbae = 0;float adbdcecaefafd = 0;float eeaeafbebcdffe = 0;float beaaaebfddc = 0;float ccaacddd = 0;float edbcadabbcacf = 0;float dcdcebebdaacef = 0;float ffbfdcddecfd = 0;float dbeecebadaabf = 0;float bffdeaedacfbc = 0;float fbbabbffef = 0;float caeaecefacb = 0;float defdcffaacae = 0;float bbefffedddcaecb = 0;float afadcfddcfadd = 0;float beeefcbffcedeba = 0;float bddbaebbbadd = 0;float facbbdfeffc = 0;float bddecdcacedacd = 0;float bdbddffae = 0;float cfaeefbad = 0;float dbbaaedefe = 0;float fbefbdacfeaadae = 0;float eabcafceedacbb = 0;float caccefacfaea = 0;float fbfcddafee = 0;float bbcbecdacd = 0;float fbcdeffceabcfbdeecddb = 0;float ddaadedbceaaa = 0;float cbbadedfafbc = 0;float cdedccefecdcacaee = 0;

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
	// input1.update();
	movie1.update();

	using namespace boost::interprocess;

    // Open the shared memory object created by Python
    shared_memory_object shm(open_only, "psm_9765373c", read_only);  // Replace with the actual name printed by the Python script

    // Map the whole shared memory in this process
    mapped_region region(shm, read_only);

    // Read data from the shared memory
    char* receivedData = static_cast<char*>(region.get_address());

	std::string reload = "RELOAD";
	std::string str;
    str = receivedData;  // Assign char* to std::string

    // std::cout << "Read from shared memory: " << receivedData << std::endl;
	if (str.substr(0, 6) == reload){
		 std::cout << "RELOADING" << std::endl;
		 shader1.load("shadersES2/shader1");
		 shader1.setUniform1f("caafbbbaa", caafbbbaa);
shader1.setUniform1f("efffdbfacedcdc", efffdbfacedcdc);
shader1.setUniform1f("dcadeccabcbbaebef", dcadeccabcbbaebef);
shader1.setUniform1f("fffaadfddd", fffaadfddd);
shader1.setUniform1f("fbcbdefbbda", fbcbdefbbda);
shader1.setUniform1f("dbececfedce", dbececfedce);
shader1.setUniform1f("efbdeabbe", efbdeabbe);
shader1.setUniform1f("ffbabcefabaabfdcf", ffbabcefabaabfdcf);
shader1.setUniform1f("ddbdefaeaac", ddbdefaeaac);
shader1.setUniform1f("efaaaeefefbae", efaaaeefefbae);
shader1.setUniform1f("adbdcecaefafd", adbdcecaefafd);
shader1.setUniform1f("eeaeafbebcdffe", eeaeafbebcdffe);
shader1.setUniform1f("beaaaebfddc", beaaaebfddc);
shader1.setUniform1f("ccaacddd", ccaacddd);
shader1.setUniform1f("edbcadabbcacf", edbcadabbcacf);
shader1.setUniform1f("dcdcebebdaacef", dcdcebebdaacef);
shader1.setUniform1f("ffbfdcddecfd", ffbfdcddecfd);
shader1.setUniform1f("dbeecebadaabf", dbeecebadaabf);
shader1.setUniform1f("bffdeaedacfbc", bffdeaedacfbc);
shader1.setUniform1f("fbbabbffef", fbbabbffef);
shader1.setUniform1f("caeaecefacb", caeaecefacb);
shader1.setUniform1f("defdcffaacae", defdcffaacae);
shader1.setUniform1f("bbefffedddcaecb", bbefffedddcaecb);
shader1.setUniform1f("afadcfddcfadd", afadcfddcfadd);
shader1.setUniform1f("beeefcbffcedeba", beeefcbffcedeba);
shader1.setUniform1f("bddbaebbbadd", bddbaebbbadd);
shader1.setUniform1f("facbbdfeffc", facbbdfeffc);
shader1.setUniform1f("bddecdcacedacd", bddecdcacedacd);
shader1.setUniform1f("bdbddffae", bdbddffae);
shader1.setUniform1f("cfaeefbad", cfaeefbad);
shader1.setUniform1f("dbbaaedefe", dbbaaedefe);
shader1.setUniform1f("fbefbdacfeaadae", fbefbdacfeaadae);
shader1.setUniform1f("eabcafceedacbb", eabcafceedacbb);
shader1.setUniform1f("caccefacfaea", caccefacfaea);
shader1.setUniform1f("fbfcddafee", fbfcddafee);
shader1.setUniform1f("bbcbecdacd", bbcbecdacd);
shader1.setUniform1f("fbcdeffceabcfbdeecddb", fbcdeffceabcfbdeecddb);
shader1.setUniform1f("ddaadedbceaaa", ddaadedbceaaa);
shader1.setUniform1f("cbbadedfafbc", cbbadedfafbc);
shader1.setUniform1f("cdedccefecdcacaee", cdedccefecdcacaee);

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
			// std::cerr << "Invalid argument: " << e.what() << std::endl;
		} catch (const std::out_of_range& e) {
			std::cerr << "Out of range: " << e.what() << std::endl;
		}

		if (varName == "caafbbbaa"){caafbbbaa= varValue;}if (varName == "efffdbfacedcdc"){efffdbfacedcdc= varValue;}if (varName == "dcadeccabcbbaebef"){dcadeccabcbbaebef= varValue;}if (varName == "fffaadfddd"){fffaadfddd= varValue;}if (varName == "fbcbdefbbda"){fbcbdefbbda= varValue;}if (varName == "dbececfedce"){dbececfedce= varValue;}if (varName == "efbdeabbe"){efbdeabbe= varValue;}if (varName == "ffbabcefabaabfdcf"){ffbabcefabaabfdcf= varValue;}if (varName == "ddbdefaeaac"){ddbdefaeaac= varValue;}if (varName == "efaaaeefefbae"){efaaaeefefbae= varValue;}if (varName == "adbdcecaefafd"){adbdcecaefafd= varValue;}if (varName == "eeaeafbebcdffe"){eeaeafbebcdffe= varValue;}if (varName == "beaaaebfddc"){beaaaebfddc= varValue;}if (varName == "ccaacddd"){ccaacddd= varValue;}if (varName == "edbcadabbcacf"){edbcadabbcacf= varValue;}if (varName == "dcdcebebdaacef"){dcdcebebdaacef= varValue;}if (varName == "ffbfdcddecfd"){ffbfdcddecfd= varValue;}if (varName == "dbeecebadaabf"){dbeecebadaabf= varValue;}if (varName == "bffdeaedacfbc"){bffdeaedacfbc= varValue;}if (varName == "fbbabbffef"){fbbabbffef= varValue;}if (varName == "caeaecefacb"){caeaecefacb= varValue;}if (varName == "defdcffaacae"){defdcffaacae= varValue;}if (varName == "bbefffedddcaecb"){bbefffedddcaecb= varValue;}if (varName == "afadcfddcfadd"){afadcfddcfadd= varValue;}if (varName == "beeefcbffcedeba"){beeefcbffcedeba= varValue;}if (varName == "bddbaebbbadd"){bddbaebbbadd= varValue;}if (varName == "facbbdfeffc"){facbbdfeffc= varValue;}if (varName == "bddecdcacedacd"){bddecdcacedacd= varValue;}if (varName == "bdbddffae"){bdbddffae= varValue;}if (varName == "cfaeefbad"){cfaeefbad= varValue;}if (varName == "dbbaaedefe"){dbbaaedefe= varValue;}if (varName == "fbefbdacfeaadae"){fbefbdacfeaadae= varValue;}if (varName == "eabcafceedacbb"){eabcafceedacbb= varValue;}if (varName == "caccefacfaea"){caccefacfaea= varValue;}if (varName == "fbfcddafee"){fbfcddafee= varValue;}if (varName == "bbcbecdacd"){bbcbecdacd= varValue;}if (varName == "fbcdeffceabcfbdeecddb"){fbcdeffceabcfbdeecddb= varValue;}if (varName == "ddaadedbceaaa"){ddaadedbceaaa= varValue;}if (varName == "cbbadedfafbc"){cbbadedfafbc= varValue;}if (varName == "cdedccefecdcacaee"){cdedccefecdcacaee= varValue;}
	}



	scaledVol = ofMap(smoothedVol, 0.0, 0.17, 0.0, 1.0, true);

	volHistory.push_back( scaledVol );
	
	if( volHistory.size() >= 400 ){
		volHistory.erase(volHistory.begin(), volHistory.begin()+1);
	}
}
//--------------------------------------------------------------
void ofApp::draw() {

	time1 += 0.01;

	framebuffer0.begin();
	shader1.begin();
	framebuffer1.draw(0, 0);

	// shader1.setUniformTexture("input1", input1.getTexture(), 1); // "1" must be incremented with multiple inputs
	shader1.setUniformTexture("input1", movie1.getTexture(), 1); // "1" must be incremented with multiple inputs
	shader1.setUniform2f("resolution", 720, 480);
	shader1.setUniform1f("time", time1);
	shader1.setUniform1f("audio", scaledVol);


	shader1.setUniform1f("caafbbbaa", caafbbbaa);
shader1.setUniform1f("efffdbfacedcdc", efffdbfacedcdc);
shader1.setUniform1f("dcadeccabcbbaebef", dcadeccabcbbaebef);
shader1.setUniform1f("fffaadfddd", fffaadfddd);
shader1.setUniform1f("fbcbdefbbda", fbcbdefbbda);
shader1.setUniform1f("dbececfedce", dbececfedce);
shader1.setUniform1f("efbdeabbe", efbdeabbe);
shader1.setUniform1f("ffbabcefabaabfdcf", ffbabcefabaabfdcf);
shader1.setUniform1f("ddbdefaeaac", ddbdefaeaac);
shader1.setUniform1f("efaaaeefefbae", efaaaeefefbae);
shader1.setUniform1f("adbdcecaefafd", adbdcecaefafd);
shader1.setUniform1f("eeaeafbebcdffe", eeaeafbebcdffe);
shader1.setUniform1f("beaaaebfddc", beaaaebfddc);
shader1.setUniform1f("ccaacddd", ccaacddd);
shader1.setUniform1f("edbcadabbcacf", edbcadabbcacf);
shader1.setUniform1f("dcdcebebdaacef", dcdcebebdaacef);
shader1.setUniform1f("ffbfdcddecfd", ffbfdcddecfd);
shader1.setUniform1f("dbeecebadaabf", dbeecebadaabf);
shader1.setUniform1f("bffdeaedacfbc", bffdeaedacfbc);
shader1.setUniform1f("fbbabbffef", fbbabbffef);
shader1.setUniform1f("caeaecefacb", caeaecefacb);
shader1.setUniform1f("defdcffaacae", defdcffaacae);
shader1.setUniform1f("bbefffedddcaecb", bbefffedddcaecb);
shader1.setUniform1f("afadcfddcfadd", afadcfddcfadd);
shader1.setUniform1f("beeefcbffcedeba", beeefcbffcedeba);
shader1.setUniform1f("bddbaebbbadd", bddbaebbbadd);
shader1.setUniform1f("facbbdfeffc", facbbdfeffc);
shader1.setUniform1f("bddecdcacedacd", bddecdcacedacd);
shader1.setUniform1f("bdbddffae", bdbddffae);
shader1.setUniform1f("cfaeefbad", cfaeefbad);
shader1.setUniform1f("dbbaaedefe", dbbaaedefe);
shader1.setUniform1f("fbefbdacfeaadae", fbefbdacfeaadae);
shader1.setUniform1f("eabcafceedacbb", eabcafceedacbb);
shader1.setUniform1f("caccefacfaea", caccefacfaea);
shader1.setUniform1f("fbfcddafee", fbfcddafee);
shader1.setUniform1f("bbcbecdacd", bbcbecdacd);
shader1.setUniform1f("fbcdeffceabcfbdeecddb", fbcdeffceabcfbdeecddb);
shader1.setUniform1f("ddaadedbceaaa", ddaadedbceaaa);
shader1.setUniform1f("cbbadedfafbc", cbbadedfafbc);
shader1.setUniform1f("cdedccefecdcacaee", cdedccefecdcacaee);


	shader1.end();

	framebuffer0.end();
	
	framebuffer0.draw(0,0,720,480);

	framebuffer1.begin();
	framebuffer0.draw(0, 0);
	framebuffer1.end();

}

//--------------------------------------------------------------
void ofApp::exit() {

}

void ofApp::audioIn(ofSoundBuffer & input){
	
	float curVol = 0.0;
	
	int numCounted = 0;	

	for (size_t i = 0; i < input.getNumFrames(); i++){
		left[i]		= input[i*2]*0.5;
		right[i]	= input[i*2+1]*0.5;

		curVol += left[i] * left[i];
		curVol += right[i] * right[i];
		numCounted+=2;
	}
	
	curVol /= (float)numCounted;
	curVol = sqrt( curVol );
	
	smoothedVol *= 0.93;
	smoothedVol += 0.07 * curVol;
	
	bufferCounter++;
	
}


//--------------------------------------------------------------
void ofApp::keyPressed(int key) {
	
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key) {
	
}

