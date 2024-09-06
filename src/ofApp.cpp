#include "ofApp.h"

#include "iostream"

#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>

#define MIDI_MAGIC 63.50f
#define CONTROL_THRESHOLD .04f


float fccdedcbdadee = 0;float dacfaebcb = 0;float abaefcbffaee = 0;float cbbaeb = 0;float ecbacbcffbefd = 0;float feabbdddbff = 0;float cbfac = 0;float efcefcbefdeaab = 0;float cfacecaebe = 0;float fabbeedfebcc = 0;float abcfbbaaabaca = 0;float edeceefbcfac = 0;float ebfcbbabfceaf = 0;float bcbbaeda = 0;float ccaeabeaadcb = 0;float edaacdadcd = 0;float fbdaebedecfde = 0;float dafccebcfdeafdf = 0;float ccbfafffbcaefaf = 0;float bbfccbfddec = 0;float bacfdbefaffcaa = 0;float caedbbfdaaa = 0;float dcaaddcad = 0;float dbedbbfafbbf = 0;float cbcdcabeef = 0;float afbaadcdfccc = 0;float febabbeb = 0;float fefcaee = 0;float edcedfdefaeaf = 0;float cffacbabced = 0;float bffccfbcfcece = 0;float bafdeabbbdbbe = 0;float ebdbcaccebbbc = 0;float cbdadedbcfc = 0;float cddfabbccb = 0;float dfabffefdbf = 0;float fdbbaaaaccde = 0;float ffbdcfbcbea = 0;float fedddaaededcaaea = 0;float efbfdfdaded = 0;

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
    shared_memory_object shm(open_only, "psm_79bf4d22", read_only);  // Replace with the actual name printed by the Python script

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
		 shader1.setUniform1f("fccdedcbdadee", fccdedcbdadee);
shader1.setUniform1f("dacfaebcb", dacfaebcb);
shader1.setUniform1f("abaefcbffaee", abaefcbffaee);
shader1.setUniform1f("cbbaeb", cbbaeb);
shader1.setUniform1f("ecbacbcffbefd", ecbacbcffbefd);
shader1.setUniform1f("feabbdddbff", feabbdddbff);
shader1.setUniform1f("cbfac", cbfac);
shader1.setUniform1f("efcefcbefdeaab", efcefcbefdeaab);
shader1.setUniform1f("cfacecaebe", cfacecaebe);
shader1.setUniform1f("fabbeedfebcc", fabbeedfebcc);
shader1.setUniform1f("abcfbbaaabaca", abcfbbaaabaca);
shader1.setUniform1f("edeceefbcfac", edeceefbcfac);
shader1.setUniform1f("ebfcbbabfceaf", ebfcbbabfceaf);
shader1.setUniform1f("bcbbaeda", bcbbaeda);
shader1.setUniform1f("ccaeabeaadcb", ccaeabeaadcb);
shader1.setUniform1f("edaacdadcd", edaacdadcd);
shader1.setUniform1f("fbdaebedecfde", fbdaebedecfde);
shader1.setUniform1f("dafccebcfdeafdf", dafccebcfdeafdf);
shader1.setUniform1f("ccbfafffbcaefaf", ccbfafffbcaefaf);
shader1.setUniform1f("bbfccbfddec", bbfccbfddec);
shader1.setUniform1f("bacfdbefaffcaa", bacfdbefaffcaa);
shader1.setUniform1f("caedbbfdaaa", caedbbfdaaa);
shader1.setUniform1f("dcaaddcad", dcaaddcad);
shader1.setUniform1f("dbedbbfafbbf", dbedbbfafbbf);
shader1.setUniform1f("cbcdcabeef", cbcdcabeef);
shader1.setUniform1f("afbaadcdfccc", afbaadcdfccc);
shader1.setUniform1f("febabbeb", febabbeb);
shader1.setUniform1f("fefcaee", fefcaee);
shader1.setUniform1f("edcedfdefaeaf", edcedfdefaeaf);
shader1.setUniform1f("cffacbabced", cffacbabced);
shader1.setUniform1f("bffccfbcfcece", bffccfbcfcece);
shader1.setUniform1f("bafdeabbbdbbe", bafdeabbbdbbe);
shader1.setUniform1f("ebdbcaccebbbc", ebdbcaccebbbc);
shader1.setUniform1f("cbdadedbcfc", cbdadedbcfc);
shader1.setUniform1f("cddfabbccb", cddfabbccb);
shader1.setUniform1f("dfabffefdbf", dfabffefdbf);
shader1.setUniform1f("fdbbaaaaccde", fdbbaaaaccde);
shader1.setUniform1f("ffbdcfbcbea", ffbdcfbcbea);
shader1.setUniform1f("fedddaaededcaaea", fedddaaededcaaea);
shader1.setUniform1f("efbfdfdaded", efbfdfdaded);

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

		if (varName == "fccdedcbdadee"){fccdedcbdadee= varValue;}if (varName == "dacfaebcb"){dacfaebcb= varValue;}if (varName == "abaefcbffaee"){abaefcbffaee= varValue;}if (varName == "cbbaeb"){cbbaeb= varValue;}if (varName == "ecbacbcffbefd"){ecbacbcffbefd= varValue;}if (varName == "feabbdddbff"){feabbdddbff= varValue;}if (varName == "cbfac"){cbfac= varValue;}if (varName == "efcefcbefdeaab"){efcefcbefdeaab= varValue;}if (varName == "cfacecaebe"){cfacecaebe= varValue;}if (varName == "fabbeedfebcc"){fabbeedfebcc= varValue;}if (varName == "abcfbbaaabaca"){abcfbbaaabaca= varValue;}if (varName == "edeceefbcfac"){edeceefbcfac= varValue;}if (varName == "ebfcbbabfceaf"){ebfcbbabfceaf= varValue;}if (varName == "bcbbaeda"){bcbbaeda= varValue;}if (varName == "ccaeabeaadcb"){ccaeabeaadcb= varValue;}if (varName == "edaacdadcd"){edaacdadcd= varValue;}if (varName == "fbdaebedecfde"){fbdaebedecfde= varValue;}if (varName == "dafccebcfdeafdf"){dafccebcfdeafdf= varValue;}if (varName == "ccbfafffbcaefaf"){ccbfafffbcaefaf= varValue;}if (varName == "bbfccbfddec"){bbfccbfddec= varValue;}if (varName == "bacfdbefaffcaa"){bacfdbefaffcaa= varValue;}if (varName == "caedbbfdaaa"){caedbbfdaaa= varValue;}if (varName == "dcaaddcad"){dcaaddcad= varValue;}if (varName == "dbedbbfafbbf"){dbedbbfafbbf= varValue;}if (varName == "cbcdcabeef"){cbcdcabeef= varValue;}if (varName == "afbaadcdfccc"){afbaadcdfccc= varValue;}if (varName == "febabbeb"){febabbeb= varValue;}if (varName == "fefcaee"){fefcaee= varValue;}if (varName == "edcedfdefaeaf"){edcedfdefaeaf= varValue;}if (varName == "cffacbabced"){cffacbabced= varValue;}if (varName == "bffccfbcfcece"){bffccfbcfcece= varValue;}if (varName == "bafdeabbbdbbe"){bafdeabbbdbbe= varValue;}if (varName == "ebdbcaccebbbc"){ebdbcaccebbbc= varValue;}if (varName == "cbdadedbcfc"){cbdadedbcfc= varValue;}if (varName == "cddfabbccb"){cddfabbccb= varValue;}if (varName == "dfabffefdbf"){dfabffefdbf= varValue;}if (varName == "fdbbaaaaccde"){fdbbaaaaccde= varValue;}if (varName == "ffbdcfbcbea"){ffbdcfbcbea= varValue;}if (varName == "fedddaaededcaaea"){fedddaaededcaaea= varValue;}if (varName == "efbfdfdaded"){efbfdfdaded= varValue;}
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


	shader1.setUniform1f("fccdedcbdadee", fccdedcbdadee);
shader1.setUniform1f("dacfaebcb", dacfaebcb);
shader1.setUniform1f("abaefcbffaee", abaefcbffaee);
shader1.setUniform1f("cbbaeb", cbbaeb);
shader1.setUniform1f("ecbacbcffbefd", ecbacbcffbefd);
shader1.setUniform1f("feabbdddbff", feabbdddbff);
shader1.setUniform1f("cbfac", cbfac);
shader1.setUniform1f("efcefcbefdeaab", efcefcbefdeaab);
shader1.setUniform1f("cfacecaebe", cfacecaebe);
shader1.setUniform1f("fabbeedfebcc", fabbeedfebcc);
shader1.setUniform1f("abcfbbaaabaca", abcfbbaaabaca);
shader1.setUniform1f("edeceefbcfac", edeceefbcfac);
shader1.setUniform1f("ebfcbbabfceaf", ebfcbbabfceaf);
shader1.setUniform1f("bcbbaeda", bcbbaeda);
shader1.setUniform1f("ccaeabeaadcb", ccaeabeaadcb);
shader1.setUniform1f("edaacdadcd", edaacdadcd);
shader1.setUniform1f("fbdaebedecfde", fbdaebedecfde);
shader1.setUniform1f("dafccebcfdeafdf", dafccebcfdeafdf);
shader1.setUniform1f("ccbfafffbcaefaf", ccbfafffbcaefaf);
shader1.setUniform1f("bbfccbfddec", bbfccbfddec);
shader1.setUniform1f("bacfdbefaffcaa", bacfdbefaffcaa);
shader1.setUniform1f("caedbbfdaaa", caedbbfdaaa);
shader1.setUniform1f("dcaaddcad", dcaaddcad);
shader1.setUniform1f("dbedbbfafbbf", dbedbbfafbbf);
shader1.setUniform1f("cbcdcabeef", cbcdcabeef);
shader1.setUniform1f("afbaadcdfccc", afbaadcdfccc);
shader1.setUniform1f("febabbeb", febabbeb);
shader1.setUniform1f("fefcaee", fefcaee);
shader1.setUniform1f("edcedfdefaeaf", edcedfdefaeaf);
shader1.setUniform1f("cffacbabced", cffacbabced);
shader1.setUniform1f("bffccfbcfcece", bffccfbcfcece);
shader1.setUniform1f("bafdeabbbdbbe", bafdeabbbdbbe);
shader1.setUniform1f("ebdbcaccebbbc", ebdbcaccebbbc);
shader1.setUniform1f("cbdadedbcfc", cbdadedbcfc);
shader1.setUniform1f("cddfabbccb", cddfabbccb);
shader1.setUniform1f("dfabffefdbf", dfabffefdbf);
shader1.setUniform1f("fdbbaaaaccde", fdbbaaaaccde);
shader1.setUniform1f("ffbdcfbcbea", ffbdcfbcbea);
shader1.setUniform1f("fedddaaededcaaea", fedddaaededcaaea);
shader1.setUniform1f("efbfdfdaded", efbfdfdaded);


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

