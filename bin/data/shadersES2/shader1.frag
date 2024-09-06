OF_GLSL_SHADER_HEADER
uniform float eebfdddbc;
uniform float aeefdadddc;
uniform float cfaffdadeface;
uniform float eafafebdbb;
uniform float dcceeebb;
uniform float dbbcbafe;
uniform float fbdbeefbfffff;
uniform float dbadbbbcfac;
uniform float bbefeeafadcea;
uniform float efeecadeadfe;
uniform float bddadcbeeeab;
uniform float dcaffadfa;
uniform float ecabeadbbbfea;
uniform float cfffdbefaeff;
uniform float cdeebeddbbc;
uniform float cbbaaedffeecba;
uniform float abbebeeaaefc;
uniform float fabccbbefcbdcf;
uniform float bbdfbaaaeca;
uniform float aeefaedcebebd;
uniform float fccacdeeeadafcedd;
uniform float babae;
uniform float ceefddaddacbc;
uniform float dcdcecdafc;
uniform float dfacaeff;
uniform float fbdffbdcedbbea;
uniform float dbacbecccbcfcefdb;
uniform float aebaacaeaacfb;
uniform float bdabdeadafdbbcefdeccfa;
uniform float fafbaeadcadebbfdeb;
uniform float edafdbedce;
uniform float eafaddfedcdb;
uniform float beaedcacffafb;
uniform float dfeceabedbc;
uniform float cbbabaacf;
uniform float dceccefdefdfeb;
uniform float fdcccaa;
uniform float daeccffaae;
uniform float bcffaafaadff;
uniform float edebdffdaaf;
uniform float time;
uniform float audio;


uniform sampler2DRect tex0;
uniform sampler2DRect maskTex;
uniform sampler2DRect input1;
uniform vec2 resolution;



in vec2 texCoordVarying;

out vec4 outputColor;

float windowWidth = 640;
float windowHeight = 480;


float colorx=texCoordVarying.x / windowWidth;
float colory=texCoordVarying.y / windowHeight;

float oscillator(in float amp, in float rate, in float frequency, in float waveShape){
	float osc = 0;
	if (waveShape == 0){
		osc = amp * fract(frequency + rate);
	}else if (waveShape == 1){ // Sin wave
		osc = amp * sin(frequency + rate);
	}else if (waveShape == 2){ // Square wave
		osc = amp * sin(frequency + rate);
		if (osc > 0){
			osc = 1;
		}else{
			osc = 0;
		}
	}else{
		float osc1 = amp * fract(frequency + rate);
		float osc2 = amp * sin(frequency + rate);
		osc = mix(osc1, osc2, waveShape);
	}
	return osc;
}

float circleOscillator(in float amp, in float frequency){
	float osc = fract(distance(vec2(texCoordVarying.x / windowWidth*1.1, texCoordVarying.y / windowHeight*1.1), vec2(0.5, 0.5)) * frequency) * amp;
	return osc;
}
 
vec3 rgb2hsb(in vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
    
    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsb2rgb(in vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

vec2 feedbackZoom(in vec2 feedbackCoords, in float zoomFactor){
	feedbackCoords-=vec2(720/2, 420/2);
	feedbackCoords=feedbackCoords*(zoomFactor);
	feedbackCoords+=vec2(720/2, 420/2);
	return feedbackCoords;
}

vec4 colorDisplaceHsb(in vec4 feedbackColor, in float x, in float y, in float z){
	vec3 feedbackColorHsb = rgb2hsb(feedbackColor.rgb);
	feedbackColorHsb += vec3(x, y, z);
	feedbackColor.rgb = hsb2rgb(feedbackColorHsb);
	return feedbackColor;
}

vec3 addColor(in vec4 color1, in vec4 color2){
	return abs(color1.rgb + color2.rgb);
}

vec3 multiplyColor(in vec4 color1, in vec4 color2){
	return abs(color1.rgb * color2.rgb);
}

vec3 lumaKey(in vec4 defaultColor, in vec4 alternativeColor, in float lumaKeyValue){
	vec4 outColor = defaultColor;
	float topLuma = .299*defaultColor.r +.587*defaultColor.g + .114*defaultColor.b;
	// float lumaKeyValue = abs(sin(time1));
	// // float lumaKeyValue = nano1;

	if (topLuma<lumaKeyValue){
		outColor.rgb=alternativeColor.rgb;
	}

	return outColor.rgb;
}


void main()
{

vec4 abfbaefadbf = vec4(0, 0, 0, 0);
vec4 bbaaefacfdb = vec4(0, 0, 0, 0);
vec2 dafcaafcacffeabc = vec2(0, 0);vec4 dafcaafcacffe = vec4(0, 0, 0, 0);
vec2 bbefbffabdabeebabc = texCoordVarying;vec4 bbefbffabdabeeb = texture(input1, bbefbffabdabeebabc);














































dafcaafcacffeabc = texCoordVarying;dafcaafcacffeabc = feedbackZoom(dafcaafcacffeabc, edebdffdaaf);dafcaafcacffe = texture(tex0, dafcaafcacffeabc);

bbaaefacfdb = colorDisplaceHsb(dafcaafcacffe, daeccffaae, dceccefdefdfeb, dfeceabedbc);

abfbaefadbf = vec4(lumaKey(bbefbffabdabeeb, bbaaefacfdb, eafaddfedcdb), 1.0);
outputColor = abfbaefadbf;
}