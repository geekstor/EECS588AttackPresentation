import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import nl.captcha.Captcha;
import nl.captcha.Captcha.Builder;
import nl.captcha.backgrounds.GradiatedBackgroundProducer;
import nl.captcha.backgrounds.SquigglesBackgroundProducer;
import nl.captcha.gimpy.DropShadowGimpyRenderer;
import nl.captcha.gimpy.FishEyeGimpyRenderer;
import nl.captcha.noise.CurvedLineNoiseProducer;
import nl.captcha.noise.StraightLineNoiseProducer;
import nl.captcha.text.producer.DefaultTextProducer;
import nl.captcha.text.renderer.ColoredEdgesWordRenderer;

public class CaptchaOutlineMain {
	public String main(boolean test, int length, int width, int height, int back, int straight, int curved, int shadow, String filename, String dirname) {
		// TODO Auto-generated method stub
		Builder builder = new Captcha.Builder(width, height);

		char[] characters = new char[26*2+10];
		for(int i = '0'; i < '0' +10; ++i){
			characters[i-'0'] = (char)i;
		}
		for(int i = 'a'; i <= 'z'; ++i){
			characters[i-'a'+ 10] = (char)i;
		}
		for(int i = 'A'; i <= 'Z'; ++i){
			characters[i-'A' + 36] = (char)i;
		}
		

		builder.addText(new DefaultTextProducer(length, characters), new ColoredEdgesWordRenderer());
		
		
		if(back == 0){
			builder.addBackground();
		}
		if(back == 1){
			builder.addBackground(new GradiatedBackgroundProducer());
		}
		
		if(curved == 1){
			builder.addNoise(new CurvedLineNoiseProducer());
		}
		if(straight == 1){
			builder.addNoise(new StraightLineNoiseProducer());
		}
		
		if(shadow == 1){
			builder.gimp(new DropShadowGimpyRenderer());
		}
		
		
		Captcha captcha = builder.build();
		
		BufferedImage im = captcha.getImage();
		
		// Remove transparency from .png, was causing it to appear as black image
		BufferedImage copy = new BufferedImage(im.getWidth(), im.getHeight(), BufferedImage.TYPE_INT_RGB);
		Graphics2D g2d = copy.createGraphics();
		g2d.setColor(Color.WHITE); // Or what ever fill color you want...
		g2d.fillRect(0, 0, copy.getWidth(), copy.getHeight());
		g2d.drawImage(im, 0, 0, null);
		g2d.dispose();
		
		// create new file to store image
		File outputfile = new File(dirname + filename);
		try {
			ImageIO.write(copy, "png", outputfile);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		if(!test){
			return captcha.getAnswer();
		}
		else{
			return "";
		}
	}
}
