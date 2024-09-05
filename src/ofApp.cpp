#include "ofApp.h"

#include "iostream"

#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <cstring>

#define MIDI_MAGIC 63.50f
#define CONTROL_THRESHOLD .04f


float ccbbcfdeebe = 0;float ddbcabebccbd = 0;float edddbcfcbbc = 0;float dfbbfaec = 0;float fbdeabbedc = 0;float fbecefbefaccf = 0;float bcabdcbaabfbbeed = 0;float edcefcdafceff = 0;float bebcceaecdf = 0;float fbacdffecb = 0;float cbcffedbadaffbbeac = 0;float cfeacaefbaabbfec = 0;float ecabbaafadefd = 0;float fdaffbbddabad = 0;float fdedfcebbfaabd = 0;float ccfffeadeac = 0;float abaacfeba = 0;float edfafbfde = 0;float afbeaacbacdfaabb = 0;float ecdfbdbeac = 0;float acdbdcbaedbe = 0;float acfdacfaca = 0;float accaaabcf = 0;float decccfacffdee = 0;float aedfddebbeafd = 0;float fdaabaaebacedcdf = 0;float cdfadaabfcded = 0;float dacdffaeeed = 0;float eddbfbebeb = 0;float afbffcebcee = 0;float fabbdbfcef = 0;float aeadfffea = 0;float eeaabbcecee = 0;float fbeaeac = 0;float cfdaeecaaefad = 0;float fbcaabebebd = 0;float fabbefaacabdbbaa = 0;float ceabbaccfdf = 0;float becaded = 0;float fecccefbaaa = 0;

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
    shared_memory_object shm(open_only, "psm_00a56908", read_only);  // Replace with the actual name printed by the Python script

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
		 shader1.setUniform1f("ccbbcfdeebe", ccbbcfdeebe);
shader1.setUniform1f("ddbcabebccbd", ddbcabebccbd);
shader1.setUniform1f("edddbcfcbbc", edddbcfcbbc);
shader1.setUniform1f("dfbbfaec", dfbbfaec);
shader1.setUniform1f("fbdeabbedc", fbdeabbedc);
shader1.setUniform1f("fbecefbefaccf", fbecefbefaccf);
shader1.setUniform1f("bcabdcbaabfbbeed", bcabdcbaabfbbeed);
shader1.setUniform1f("edcefcdafceff", edcefcdafceff);
shader1.setUniform1f("bebcceaecdf", bebcceaecdf);
shader1.setUniform1f("fbacdffecb", fbacdffecb);
shader1.setUniform1f("cbcffedbadaffbbeac", cbcffedbadaffbbeac);
shader1.setUniform1f("cfeacaefbaabbfec", cfeacaefbaabbfec);
shader1.setUniform1f("ecabbaafadefd", ecabbaafadefd);
shader1.setUniform1f("fdaffbbddabad", fdaffbbddabad);
shader1.setUniform1f("fdedfcebbfaabd", fdedfcebbfaabd);
shader1.setUniform1f("ccfffeadeac", ccfffeadeac);
shader1.setUniform1f("abaacfeba", abaacfeba);
shader1.setUniform1f("edfafbfde", edfafbfde);
shader1.setUniform1f("afbeaacbacdfaabb", afbeaacbacdfaabb);
shader1.setUniform1f("ecdfbdbeac", ecdfbdbeac);
shader1.setUniform1f("acdbdcbaedbe", acdbdcbaedbe);
shader1.setUniform1f("acfdacfaca", acfdacfaca);
shader1.setUniform1f("accaaabcf", accaaabcf);
shader1.setUniform1f("decccfacffdee", decccfacffdee);
shader1.setUniform1f("aedfddebbeafd", aedfddebbeafd);
shader1.setUniform1f("fdaabaaebacedcdf", fdaabaaebacedcdf);
shader1.setUniform1f("cdfadaabfcded", cdfadaabfcded);
shader1.setUniform1f("dacdffaeeed", dacdffaeeed);
shader1.setUniform1f("eddbfbebeb", eddbfbebeb);
shader1.setUniform1f("afbffcebcee", afbffcebcee);
shader1.setUniform1f("fabbdbfcef", fabbdbfcef);
shader1.setUniform1f("aeadfffea", aeadfffea);
shader1.setUniform1f("eeaabbcecee", eeaabbcecee);
shader1.setUniform1f("fbeaeac", fbeaeac);
shader1.setUniform1f("cfdaeecaaefad", cfdaeecaaefad);
shader1.setUniform1f("fbcaabebebd", fbcaabebebd);
shader1.setUniform1f("fabbefaacabdbbaa", fabbefaacabdbbaa);
shader1.setUniform1f("ceabbaccfdf", ceabbaccfdf);
shader1.setUniform1f("becaded", becaded);
shader1.setUniform1f("fecccefbaaa", fecccefbaaa);

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

		if (varName == "ccbbcfdeebe"){ccbbcfdeebe= varValue;}if (varName == "ddbcabebccbd"){ddbcabebccbd= varValue;}if (varName == "edddbcfcbbc"){edddbcfcbbc= varValue;}if (varName == "dfbbfaec"){dfbbfaec= varValue;}if (varName == "fbdeabbedc"){fbdeabbedc= varValue;}if (varName == "fbecefbefaccf"){fbecefbefaccf= varValue;}if (varName == "bcabdcbaabfbbeed"){bcabdcbaabfbbeed= varValue;}if (varName == "edcefcdafceff"){edcefcdafceff= varValue;}if (varName == "bebcceaecdf"){bebcceaecdf= varValue;}if (varName == "fbacdffecb"){fbacdffecb= varValue;}if (varName == "cbcffedbadaffbbeac"){cbcffedbadaffbbeac= varValue;}if (varName == "cfeacaefbaabbfec"){cfeacaefbaabbfec= varValue;}if (varName == "ecabbaafadefd"){ecabbaafadefd= varValue;}if (varName == "fdaffbbddabad"){fdaffbbddabad= varValue;}if (varName == "fdedfcebbfaabd"){fdedfcebbfaabd= varValue;}if (varName == "ccfffeadeac"){ccfffeadeac= varValue;}if (varName == "abaacfeba"){abaacfeba= varValue;}if (varName == "edfafbfde"){edfafbfde= varValue;}if (varName == "afbeaacbacdfaabb"){afbeaacbacdfaabb= varValue;}if (varName == "ecdfbdbeac"){ecdfbdbeac= varValue;}if (varName == "acdbdcbaedbe"){acdbdcbaedbe= varValue;}if (varName == "acfdacfaca"){acfdacfaca= varValue;}if (varName == "accaaabcf"){accaaabcf= varValue;}if (varName == "decccfacffdee"){decccfacffdee= varValue;}if (varName == "aedfddebbeafd"){aedfddebbeafd= varValue;}if (varName == "fdaabaaebacedcdf"){fdaabaaebacedcdf= varValue;}if (varName == "cdfadaabfcded"){cdfadaabfcded= varValue;}if (varName == "dacdffaeeed"){dacdffaeeed= varValue;}if (varName == "eddbfbebeb"){eddbfbebeb= varValue;}if (varName == "afbffcebcee"){afbffcebcee= varValue;}if (varName == "fabbdbfcef"){fabbdbfcef= varValue;}if (varName == "aeadfffea"){aeadfffea= varValue;}if (varName == "eeaabbcecee"){eeaabbcecee= varValue;}if (varName == "fbeaeac"){fbeaeac= varValue;}if (varName == "cfdaeecaaefad"){cfdaeecaaefad= varValue;}if (varName == "fbcaabebebd"){fbcaabebebd= varValue;}if (varName == "fabbefaacabdbbaa"){fabbefaacabdbbaa= varValue;}if (varName == "ceabbaccfdf"){ceabbaccfdf= varValue;}if (varName == "becaded"){becaded= varValue;}if (varName == "fecccefbaaa"){fecccefbaaa= varValue;}
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
	std::cout << scaledVol << std::endl;

	shader1.setUniform1f("ccbbcfdeebe", ccbbcfdeebe);
shader1.setUniform1f("ddbcabebccbd", ddbcabebccbd);
shader1.setUniform1f("edddbcfcbbc", edddbcfcbbc);
shader1.setUniform1f("dfbbfaec", dfbbfaec);
shader1.setUniform1f("fbdeabbedc", fbdeabbedc);
shader1.setUniform1f("fbecefbefaccf", fbecefbefaccf);
shader1.setUniform1f("bcabdcbaabfbbeed", bcabdcbaabfbbeed);
shader1.setUniform1f("edcefcdafceff", edcefcdafceff);
shader1.setUniform1f("bebcceaecdf", bebcceaecdf);
shader1.setUniform1f("fbacdffecb", fbacdffecb);
shader1.setUniform1f("cbcffedbadaffbbeac", cbcffedbadaffbbeac);
shader1.setUniform1f("cfeacaefbaabbfec", cfeacaefbaabbfec);
shader1.setUniform1f("ecabbaafadefd", ecabbaafadefd);
shader1.setUniform1f("fdaffbbddabad", fdaffbbddabad);
shader1.setUniform1f("fdedfcebbfaabd", fdedfcebbfaabd);
shader1.setUniform1f("ccfffeadeac", ccfffeadeac);
shader1.setUniform1f("abaacfeba", abaacfeba);
shader1.setUniform1f("edfafbfde", edfafbfde);
shader1.setUniform1f("afbeaacbacdfaabb", afbeaacbacdfaabb);
shader1.setUniform1f("ecdfbdbeac", ecdfbdbeac);
shader1.setUniform1f("acdbdcbaedbe", acdbdcbaedbe);
shader1.setUniform1f("acfdacfaca", acfdacfaca);
shader1.setUniform1f("accaaabcf", accaaabcf);
shader1.setUniform1f("decccfacffdee", decccfacffdee);
shader1.setUniform1f("aedfddebbeafd", aedfddebbeafd);
shader1.setUniform1f("fdaabaaebacedcdf", fdaabaaebacedcdf);
shader1.setUniform1f("cdfadaabfcded", cdfadaabfcded);
shader1.setUniform1f("dacdffaeeed", dacdffaeeed);
shader1.setUniform1f("eddbfbebeb", eddbfbebeb);
shader1.setUniform1f("afbffcebcee", afbffcebcee);
shader1.setUniform1f("fabbdbfcef", fabbdbfcef);
shader1.setUniform1f("aeadfffea", aeadfffea);
shader1.setUniform1f("eeaabbcecee", eeaabbcecee);
shader1.setUniform1f("fbeaeac", fbeaeac);
shader1.setUniform1f("cfdaeecaaefad", cfdaeecaaefad);
shader1.setUniform1f("fbcaabebebd", fbcaabebebd);
shader1.setUniform1f("fabbefaacabdbbaa", fabbefaacabdbbaa);
shader1.setUniform1f("ceabbaccfdf", ceabbaccfdf);
shader1.setUniform1f("becaded", becaded);
shader1.setUniform1f("fecccefbaaa", fecccefbaaa);


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

