OF_GLSL_SHADER_HEADER
uniform float adcfacaaccdfb;
uniform float ffaaccfaecfdf;
uniform float bfffdddbedeceaf;
uniform float bfdadcefcceccdae;
uniform float ccafaabecb;
uniform float bdeeccdacafdfe;
uniform float babeacaeeced;
uniform float ddfabfefbbd;
uniform float bacabcdecba;
uniform float dacdbcbbaecfcca;
uniform float fbffafdade;
uniform float dedadefbaeecbdf;
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

vec4 eebecaabcee = vec4(0, 0, 0, 0);

vec4 cbbdbbcabafefeb = vec4(0, 0, 0, 0);
vec4 cdcebfbeec = vec4(0, 0, 0, 0);

float efcfbfdfefbcfe = 0;
vec4 adfecc = vec4(0, 0, 0, 0);
float cfeacbcfda = 0;
vec2 acbccaecfbabc = texCoordVarying;vec4 acbccaecfb = texture(input1, acbccaecfbabc);



















efcfbfdfefbcfe = bdeeccdacafdfe * colorx;

efcfbfdfefbcfe = bdeeccdacafdfe * colorx;




vec2 ebabdfbcbabc = texCoordVarying;ebabdfbcbabc = feedbackZoom(ebabdfbcbabc, bacabcdecba);vec4 ebabdfbcb = texture(tex0, ebabdfbcbabc);

cfeacbcfda = circleOscillator(fbffafdade, efcfbfdfefbcfe);
cfeacbcfda = circleOscillator(fbffafdade, efcfbfdfefbcfe);

eebecaabcee = colorDisplaceHsb(ebabdfbcb, bacabcdecba, ddfabfefbbd, babeacaeeced);

adfecc = vec4(cfeacbcfda, cfeacbcfda, ccafaabecb, 1.0);
cbbdbbcabafefeb = vec4(lumaKey(acbccaecfb, eebecaabcee, dacdbcbbaecfcca), 1.0);

cdcebfbeec = vec4(lumaKey(adfecc, cbbdbbcabafefeb, dedadefbaeecbdf), 1.0);
outputColor = cdcebfbeec;
}