#include "ofApp.h"

#include "iostream"

#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>

#define MIDI_MAGIC 63.50f
#define CONTROL_THRESHOLD .04f


float eebfdddbc = 0;float aeefdadddc = 0;float cfaffdadeface = 0;float eafafebdbb = 0;float dcceeebb = 0;float dbbcbafe = 0;float fbdbeefbfffff = 0;float dbadbbbcfac = 0;float bbefeeafadcea = 0;float efeecadeadfe = 0;float bddadcbeeeab = 0;float dcaffadfa = 0;float ecabeadbbbfea = 0;float cfffdbefaeff = 0;float cdeebeddbbc = 0;float cbbaaedffeecba = 0;float abbebeeaaefc = 0;float fabccbbefcbdcf = 0;float bbdfbaaaeca = 0;float aeefaedcebebd = 0;float fccacdeeeadafcedd = 0;float babae = 0;float ceefddaddacbc = 0;float dcdcecdafc = 0;float dfacaeff = 0;float fbdffbdcedbbea = 0;float dbacbecccbcfcefdb = 0;float aebaacaeaacfb = 0;float bdabdeadafdbbcefdeccfa = 0;float fafbaeadcadebbfdeb = 0;float edafdbedce = 0;float eafaddfedcdb = 0;float beaedcacffafb = 0;float dfeceabedbc = 0;float cbbabaacf = 0;float dceccefdefdfeb = 0;float fdcccaa = 0;float daeccffaae = 0;float bcffaafaadff = 0;float edebdffdaaf = 0;

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
    shared_memory_object shm(open_only, "psm_a793ba13", read_only);  // Replace with the actual name printed by the Python script

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
		 shader1.setUniform1f("eebfdddbc", eebfdddbc);
shader1.setUniform1f("aeefdadddc", aeefdadddc);
shader1.setUniform1f("cfaffdadeface", cfaffdadeface);
shader1.setUniform1f("eafafebdbb", eafafebdbb);
shader1.setUniform1f("dcceeebb", dcceeebb);
shader1.setUniform1f("dbbcbafe", dbbcbafe);
shader1.setUniform1f("fbdbeefbfffff", fbdbeefbfffff);
shader1.setUniform1f("dbadbbbcfac", dbadbbbcfac);
shader1.setUniform1f("bbefeeafadcea", bbefeeafadcea);
shader1.setUniform1f("efeecadeadfe", efeecadeadfe);
shader1.setUniform1f("bddadcbeeeab", bddadcbeeeab);
shader1.setUniform1f("dcaffadfa", dcaffadfa);
shader1.setUniform1f("ecabeadbbbfea", ecabeadbbbfea);
shader1.setUniform1f("cfffdbefaeff", cfffdbefaeff);
shader1.setUniform1f("cdeebeddbbc", cdeebeddbbc);
shader1.setUniform1f("cbbaaedffeecba", cbbaaedffeecba);
shader1.setUniform1f("abbebeeaaefc", abbebeeaaefc);
shader1.setUniform1f("fabccbbefcbdcf", fabccbbefcbdcf);
shader1.setUniform1f("bbdfbaaaeca", bbdfbaaaeca);
shader1.setUniform1f("aeefaedcebebd", aeefaedcebebd);
shader1.setUniform1f("fccacdeeeadafcedd", fccacdeeeadafcedd);
shader1.setUniform1f("babae", babae);
shader1.setUniform1f("ceefddaddacbc", ceefddaddacbc);
shader1.setUniform1f("dcdcecdafc", dcdcecdafc);
shader1.setUniform1f("dfacaeff", dfacaeff);
shader1.setUniform1f("fbdffbdcedbbea", fbdffbdcedbbea);
shader1.setUniform1f("dbacbecccbcfcefdb", dbacbecccbcfcefdb);
shader1.setUniform1f("aebaacaeaacfb", aebaacaeaacfb);
shader1.setUniform1f("bdabdeadafdbbcefdeccfa", bdabdeadafdbbcefdeccfa);
shader1.setUniform1f("fafbaeadcadebbfdeb", fafbaeadcadebbfdeb);
shader1.setUniform1f("edafdbedce", edafdbedce);
shader1.setUniform1f("eafaddfedcdb", eafaddfedcdb);
shader1.setUniform1f("beaedcacffafb", beaedcacffafb);
shader1.setUniform1f("dfeceabedbc", dfeceabedbc);
shader1.setUniform1f("cbbabaacf", cbbabaacf);
shader1.setUniform1f("dceccefdefdfeb", dceccefdefdfeb);
shader1.setUniform1f("fdcccaa", fdcccaa);
shader1.setUniform1f("daeccffaae", daeccffaae);
shader1.setUniform1f("bcffaafaadff", bcffaafaadff);
shader1.setUniform1f("edebdffdaaf", edebdffdaaf);

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

		if (varName == "eebfdddbc"){eebfdddbc= varValue;}if (varName == "aeefdadddc"){aeefdadddc= varValue;}if (varName == "cfaffdadeface"){cfaffdadeface= varValue;}if (varName == "eafafebdbb"){eafafebdbb= varValue;}if (varName == "dcceeebb"){dcceeebb= varValue;}if (varName == "dbbcbafe"){dbbcbafe= varValue;}if (varName == "fbdbeefbfffff"){fbdbeefbfffff= varValue;}if (varName == "dbadbbbcfac"){dbadbbbcfac= varValue;}if (varName == "bbefeeafadcea"){bbefeeafadcea= varValue;}if (varName == "efeecadeadfe"){efeecadeadfe= varValue;}if (varName == "bddadcbeeeab"){bddadcbeeeab= varValue;}if (varName == "dcaffadfa"){dcaffadfa= varValue;}if (varName == "ecabeadbbbfea"){ecabeadbbbfea= varValue;}if (varName == "cfffdbefaeff"){cfffdbefaeff= varValue;}if (varName == "cdeebeddbbc"){cdeebeddbbc= varValue;}if (varName == "cbbaaedffeecba"){cbbaaedffeecba= varValue;}if (varName == "abbebeeaaefc"){abbebeeaaefc= varValue;}if (varName == "fabccbbefcbdcf"){fabccbbefcbdcf= varValue;}if (varName == "bbdfbaaaeca"){bbdfbaaaeca= varValue;}if (varName == "aeefaedcebebd"){aeefaedcebebd= varValue;}if (varName == "fccacdeeeadafcedd"){fccacdeeeadafcedd= varValue;}if (varName == "babae"){babae= varValue;}if (varName == "ceefddaddacbc"){ceefddaddacbc= varValue;}if (varName == "dcdcecdafc"){dcdcecdafc= varValue;}if (varName == "dfacaeff"){dfacaeff= varValue;}if (varName == "fbdffbdcedbbea"){fbdffbdcedbbea= varValue;}if (varName == "dbacbecccbcfcefdb"){dbacbecccbcfcefdb= varValue;}if (varName == "aebaacaeaacfb"){aebaacaeaacfb= varValue;}if (varName == "bdabdeadafdbbcefdeccfa"){bdabdeadafdbbcefdeccfa= varValue;}if (varName == "fafbaeadcadebbfdeb"){fafbaeadcadebbfdeb= varValue;}if (varName == "edafdbedce"){edafdbedce= varValue;}if (varName == "eafaddfedcdb"){eafaddfedcdb= varValue;}if (varName == "beaedcacffafb"){beaedcacffafb= varValue;}if (varName == "dfeceabedbc"){dfeceabedbc= varValue;}if (varName == "cbbabaacf"){cbbabaacf= varValue;}if (varName == "dceccefdefdfeb"){dceccefdefdfeb= varValue;}if (varName == "fdcccaa"){fdcccaa= varValue;}if (varName == "daeccffaae"){daeccffaae= varValue;}if (varName == "bcffaafaadff"){bcffaafaadff= varValue;}if (varName == "edebdffdaaf"){edebdffdaaf= varValue;}
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


	shader1.setUniform1f("eebfdddbc", eebfdddbc);
shader1.setUniform1f("aeefdadddc", aeefdadddc);
shader1.setUniform1f("cfaffdadeface", cfaffdadeface);
shader1.setUniform1f("eafafebdbb", eafafebdbb);
shader1.setUniform1f("dcceeebb", dcceeebb);
shader1.setUniform1f("dbbcbafe", dbbcbafe);
shader1.setUniform1f("fbdbeefbfffff", fbdbeefbfffff);
shader1.setUniform1f("dbadbbbcfac", dbadbbbcfac);
shader1.setUniform1f("bbefeeafadcea", bbefeeafadcea);
shader1.setUniform1f("efeecadeadfe", efeecadeadfe);
shader1.setUniform1f("bddadcbeeeab", bddadcbeeeab);
shader1.setUniform1f("dcaffadfa", dcaffadfa);
shader1.setUniform1f("ecabeadbbbfea", ecabeadbbbfea);
shader1.setUniform1f("cfffdbefaeff", cfffdbefaeff);
shader1.setUniform1f("cdeebeddbbc", cdeebeddbbc);
shader1.setUniform1f("cbbaaedffeecba", cbbaaedffeecba);
shader1.setUniform1f("abbebeeaaefc", abbebeeaaefc);
shader1.setUniform1f("fabccbbefcbdcf", fabccbbefcbdcf);
shader1.setUniform1f("bbdfbaaaeca", bbdfbaaaeca);
shader1.setUniform1f("aeefaedcebebd", aeefaedcebebd);
shader1.setUniform1f("fccacdeeeadafcedd", fccacdeeeadafcedd);
shader1.setUniform1f("babae", babae);
shader1.setUniform1f("ceefddaddacbc", ceefddaddacbc);
shader1.setUniform1f("dcdcecdafc", dcdcecdafc);
shader1.setUniform1f("dfacaeff", dfacaeff);
shader1.setUniform1f("fbdffbdcedbbea", fbdffbdcedbbea);
shader1.setUniform1f("dbacbecccbcfcefdb", dbacbecccbcfcefdb);
shader1.setUniform1f("aebaacaeaacfb", aebaacaeaacfb);
shader1.setUniform1f("bdabdeadafdbbcefdeccfa", bdabdeadafdbbcefdeccfa);
shader1.setUniform1f("fafbaeadcadebbfdeb", fafbaeadcadebbfdeb);
shader1.setUniform1f("edafdbedce", edafdbedce);
shader1.setUniform1f("eafaddfedcdb", eafaddfedcdb);
shader1.setUniform1f("beaedcacffafb", beaedcacffafb);
shader1.setUniform1f("dfeceabedbc", dfeceabedbc);
shader1.setUniform1f("cbbabaacf", cbbabaacf);
shader1.setUniform1f("dceccefdefdfeb", dceccefdefdfeb);
shader1.setUniform1f("fdcccaa", fdcccaa);
shader1.setUniform1f("daeccffaae", daeccffaae);
shader1.setUniform1f("bcffaafaadff", bcffaafaadff);
shader1.setUniform1f("edebdffdaaf", edebdffdaaf);


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

