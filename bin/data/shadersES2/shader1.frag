OF_GLSL_SHADER_HEADER
// precision highp float;

uniform sampler2DRect tex0;
uniform sampler2DRect maskTex;
uniform sampler2DRect input1;
uniform vec2 resolution;

uniform float sx;
uniform float az;
uniform float fv;
uniform float nano1;
uniform float audio;
uniform float time1;
uniform float time2;

in vec2 texCoordVarying;

out vec4 outputColor;

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

	float windowWidth = 720;
	float windowHeight = 480;

	
	float colorx=texCoordVarying.x / windowWidth;
	float colory=texCoordVarying.y / windowHeight;

	float hOsc = oscillator(1, colorx*fv/10, audio , 0);
	float vOsc = oscillator(1, 1/(colory*(1/hOsc)), time2, 0);
	float zOsc = oscillator(1, 1/(colorx*(hOsc/vOsc*hOsc)), 0, 1); 
	// float vOsc = oscillator((1.0-sx), colory*(nano1/10+(10.0 * hOsc)), time1/2, 0);

	// float hOsc = oscillator(1, colorx*audio*fv*10, time1, 0);

	// float oscOut = hOsc;

	// vec4 oscColor = vec4(oscOut, oscOut, oscOut, 1.0);
	vec4 oscColor = vec4(hOsc/zOsc, vOsc, zOsc/hOsc, 1.0);

	// feedback
	vec2 feedbackCoords = texCoordVarying;
	feedbackCoords = feedbackZoom(feedbackCoords, 1.0+0.1*-az/10);
	// feedbackCoords.x += az;
	vec4 feedbackColor = texture(tex0, feedbackCoords);

	// colors
	// feedbackColor = colorDisplaceHsb(feedbackColor, .05, 1, .01);

	// vec2 input1Coords = texCoordVarying;
	// vec2 input1Coords = texCoordVarying * oscOut;
	// vec4 input1Color = texture(input1, input1Coords);

	// Swap and invert channels
	// input1Color.r = 1.0-input1Color.g;
	// input1Color.g = 1.0-input1Color.b;

	// input1Color.r=fract(abs(input1Color.r+2.0*sx/10*oscColor.r));
	// input1Color.g=fract(abs(input1Color.g+2.0*sx/10*oscColor.g));
	// input1Color.b=fract(abs(input1Color.b+2.0*sx/10*oscColor.b));

	oscColor = colorDisplaceHsb(oscColor, oscColor.g*sx, oscColor.b*sx, oscColor.r*sx);
	// input1Color = colorDisplaceHsb(input1Color, oscColor.r*sx, oscColor.g*sx, oscColor.b*sx);


	// Mixing
	vec4 outColor = vec4(0, 0, 0, 1);

	outColor = oscColor;

	// Lerping
	// outColor = mix(input1Color, oscColor, nano1);

	// Add or subtract
	// outColor.rgb = addColor(input1Color, oscColor);
	// outColor.rgb = multiplyColor(input1Color, oscColor);

	// lumakey
	outColor.rgb = lumaKey(outColor, feedbackColor, audio*fv);
	// outColor.rgb = lumaKey(input1Color, feedbackColor, fv);
	// outColor.rgb = lumaKey(input1Color, feedbackColor, audio*10 + 0.01);
	
	outputColor = outColor;


	// outputColor = input1Color;

	// outputColor = texture(tex0, feedbackCoords);
}
