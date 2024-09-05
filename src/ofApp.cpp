#include "ofApp.h"

#include "iostream"

#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>

#define MIDI_MAGIC 63.50f
#define CONTROL_THRESHOLD .04f


float bdbefeecefbde = 0;float faabfecbc = 0;float feabdddbbaabcbec = 0;float ceaedfebdf = 0;float ddcbabafc = 0;float eebdbebfacfa = 0;float befbbedfdbc = 0;float ececccdcfaa = 0;float afbaebcffd = 0;float cadffbfbdfccdf = 0;float cffedbfdacd = 0;float aaefaddae = 0;float bfedaeca = 0;float dbbbeadab = 0;float cfbdbfffbbcabd = 0;float aeecdfafbedcf = 0;float bfaeddbafcf = 0;float efddebdeac = 0;float babdbcbfcbacf = 0;float fdfefaecbfeeebf = 0;float fffefeacceddff = 0;float dadaecffabccabe = 0;float dedddbacacdafa = 0;float efbbaacc = 0;float ffeabfaadcbeedbd = 0;float eacbefabaabbbd = 0;float bcecbebfffac = 0;float dbbedccc = 0;float cbbddaabcd = 0;float fdababbcc = 0;float aadfadedaacdbc = 0;float dfdbacdddda = 0;float fdfcddbbcbffaaaba = 0;float bdffdcdac = 0;float cbcffbcdaa = 0;float ecdeabfedfdbbc = 0;float adecdfffaedcadfa = 0;float aedc = 0;float abfdcbcbfbc = 0;float dcdfbcfedd = 0;

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
    shared_memory_object shm(open_only, "psm_6b25b755", read_only);  // Replace with the actual name printed by the Python script

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
		 shader1.setUniform1f("bdbefeecefbde", bdbefeecefbde);
shader1.setUniform1f("faabfecbc", faabfecbc);
shader1.setUniform1f("feabdddbbaabcbec", feabdddbbaabcbec);
shader1.setUniform1f("ceaedfebdf", ceaedfebdf);
shader1.setUniform1f("ddcbabafc", ddcbabafc);
shader1.setUniform1f("eebdbebfacfa", eebdbebfacfa);
shader1.setUniform1f("befbbedfdbc", befbbedfdbc);
shader1.setUniform1f("ececccdcfaa", ececccdcfaa);
shader1.setUniform1f("afbaebcffd", afbaebcffd);
shader1.setUniform1f("cadffbfbdfccdf", cadffbfbdfccdf);
shader1.setUniform1f("cffedbfdacd", cffedbfdacd);
shader1.setUniform1f("aaefaddae", aaefaddae);
shader1.setUniform1f("bfedaeca", bfedaeca);
shader1.setUniform1f("dbbbeadab", dbbbeadab);
shader1.setUniform1f("cfbdbfffbbcabd", cfbdbfffbbcabd);
shader1.setUniform1f("aeecdfafbedcf", aeecdfafbedcf);
shader1.setUniform1f("bfaeddbafcf", bfaeddbafcf);
shader1.setUniform1f("efddebdeac", efddebdeac);
shader1.setUniform1f("babdbcbfcbacf", babdbcbfcbacf);
shader1.setUniform1f("fdfefaecbfeeebf", fdfefaecbfeeebf);
shader1.setUniform1f("fffefeacceddff", fffefeacceddff);
shader1.setUniform1f("dadaecffabccabe", dadaecffabccabe);
shader1.setUniform1f("dedddbacacdafa", dedddbacacdafa);
shader1.setUniform1f("efbbaacc", efbbaacc);
shader1.setUniform1f("ffeabfaadcbeedbd", ffeabfaadcbeedbd);
shader1.setUniform1f("eacbefabaabbbd", eacbefabaabbbd);
shader1.setUniform1f("bcecbebfffac", bcecbebfffac);
shader1.setUniform1f("dbbedccc", dbbedccc);
shader1.setUniform1f("cbbddaabcd", cbbddaabcd);
shader1.setUniform1f("fdababbcc", fdababbcc);
shader1.setUniform1f("aadfadedaacdbc", aadfadedaacdbc);
shader1.setUniform1f("dfdbacdddda", dfdbacdddda);
shader1.setUniform1f("fdfcddbbcbffaaaba", fdfcddbbcbffaaaba);
shader1.setUniform1f("bdffdcdac", bdffdcdac);
shader1.setUniform1f("cbcffbcdaa", cbcffbcdaa);
shader1.setUniform1f("ecdeabfedfdbbc", ecdeabfedfdbbc);
shader1.setUniform1f("adecdfffaedcadfa", adecdfffaedcadfa);
shader1.setUniform1f("aedc", aedc);
shader1.setUniform1f("abfdcbcbfbc", abfdcbcbfbc);
shader1.setUniform1f("dcdfbcfedd", dcdfbcfedd);

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

		if (varName == "bdbefeecefbde"){bdbefeecefbde= varValue;}if (varName == "faabfecbc"){faabfecbc= varValue;}if (varName == "feabdddbbaabcbec"){feabdddbbaabcbec= varValue;}if (varName == "ceaedfebdf"){ceaedfebdf= varValue;}if (varName == "ddcbabafc"){ddcbabafc= varValue;}if (varName == "eebdbebfacfa"){eebdbebfacfa= varValue;}if (varName == "befbbedfdbc"){befbbedfdbc= varValue;}if (varName == "ececccdcfaa"){ececccdcfaa= varValue;}if (varName == "afbaebcffd"){afbaebcffd= varValue;}if (varName == "cadffbfbdfccdf"){cadffbfbdfccdf= varValue;}if (varName == "cffedbfdacd"){cffedbfdacd= varValue;}if (varName == "aaefaddae"){aaefaddae= varValue;}if (varName == "bfedaeca"){bfedaeca= varValue;}if (varName == "dbbbeadab"){dbbbeadab= varValue;}if (varName == "cfbdbfffbbcabd"){cfbdbfffbbcabd= varValue;}if (varName == "aeecdfafbedcf"){aeecdfafbedcf= varValue;}if (varName == "bfaeddbafcf"){bfaeddbafcf= varValue;}if (varName == "efddebdeac"){efddebdeac= varValue;}if (varName == "babdbcbfcbacf"){babdbcbfcbacf= varValue;}if (varName == "fdfefaecbfeeebf"){fdfefaecbfeeebf= varValue;}if (varName == "fffefeacceddff"){fffefeacceddff= varValue;}if (varName == "dadaecffabccabe"){dadaecffabccabe= varValue;}if (varName == "dedddbacacdafa"){dedddbacacdafa= varValue;}if (varName == "efbbaacc"){efbbaacc= varValue;}if (varName == "ffeabfaadcbeedbd"){ffeabfaadcbeedbd= varValue;}if (varName == "eacbefabaabbbd"){eacbefabaabbbd= varValue;}if (varName == "bcecbebfffac"){bcecbebfffac= varValue;}if (varName == "dbbedccc"){dbbedccc= varValue;}if (varName == "cbbddaabcd"){cbbddaabcd= varValue;}if (varName == "fdababbcc"){fdababbcc= varValue;}if (varName == "aadfadedaacdbc"){aadfadedaacdbc= varValue;}if (varName == "dfdbacdddda"){dfdbacdddda= varValue;}if (varName == "fdfcddbbcbffaaaba"){fdfcddbbcbffaaaba= varValue;}if (varName == "bdffdcdac"){bdffdcdac= varValue;}if (varName == "cbcffbcdaa"){cbcffbcdaa= varValue;}if (varName == "ecdeabfedfdbbc"){ecdeabfedfdbbc= varValue;}if (varName == "adecdfffaedcadfa"){adecdfffaedcadfa= varValue;}if (varName == "aedc"){aedc= varValue;}if (varName == "abfdcbcbfbc"){abfdcbcbfbc= varValue;}if (varName == "dcdfbcfedd"){dcdfbcfedd= varValue;}
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


	shader1.setUniform1f("bdbefeecefbde", bdbefeecefbde);
shader1.setUniform1f("faabfecbc", faabfecbc);
shader1.setUniform1f("feabdddbbaabcbec", feabdddbbaabcbec);
shader1.setUniform1f("ceaedfebdf", ceaedfebdf);
shader1.setUniform1f("ddcbabafc", ddcbabafc);
shader1.setUniform1f("eebdbebfacfa", eebdbebfacfa);
shader1.setUniform1f("befbbedfdbc", befbbedfdbc);
shader1.setUniform1f("ececccdcfaa", ececccdcfaa);
shader1.setUniform1f("afbaebcffd", afbaebcffd);
shader1.setUniform1f("cadffbfbdfccdf", cadffbfbdfccdf);
shader1.setUniform1f("cffedbfdacd", cffedbfdacd);
shader1.setUniform1f("aaefaddae", aaefaddae);
shader1.setUniform1f("bfedaeca", bfedaeca);
shader1.setUniform1f("dbbbeadab", dbbbeadab);
shader1.setUniform1f("cfbdbfffbbcabd", cfbdbfffbbcabd);
shader1.setUniform1f("aeecdfafbedcf", aeecdfafbedcf);
shader1.setUniform1f("bfaeddbafcf", bfaeddbafcf);
shader1.setUniform1f("efddebdeac", efddebdeac);
shader1.setUniform1f("babdbcbfcbacf", babdbcbfcbacf);
shader1.setUniform1f("fdfefaecbfeeebf", fdfefaecbfeeebf);
shader1.setUniform1f("fffefeacceddff", fffefeacceddff);
shader1.setUniform1f("dadaecffabccabe", dadaecffabccabe);
shader1.setUniform1f("dedddbacacdafa", dedddbacacdafa);
shader1.setUniform1f("efbbaacc", efbbaacc);
shader1.setUniform1f("ffeabfaadcbeedbd", ffeabfaadcbeedbd);
shader1.setUniform1f("eacbefabaabbbd", eacbefabaabbbd);
shader1.setUniform1f("bcecbebfffac", bcecbebfffac);
shader1.setUniform1f("dbbedccc", dbbedccc);
shader1.setUniform1f("cbbddaabcd", cbbddaabcd);
shader1.setUniform1f("fdababbcc", fdababbcc);
shader1.setUniform1f("aadfadedaacdbc", aadfadedaacdbc);
shader1.setUniform1f("dfdbacdddda", dfdbacdddda);
shader1.setUniform1f("fdfcddbbcbffaaaba", fdfcddbbcbffaaaba);
shader1.setUniform1f("bdffdcdac", bdffdcdac);
shader1.setUniform1f("cbcffbcdaa", cbcffbcdaa);
shader1.setUniform1f("ecdeabfedfdbbc", ecdeabfedfdbbc);
shader1.setUniform1f("adecdfffaedcadfa", adecdfffaedcadfa);
shader1.setUniform1f("aedc", aedc);
shader1.setUniform1f("abfdcbcbfbc", abfdcbcbfbc);
shader1.setUniform1f("dcdfbcfedd", dcdfbcfedd);


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

