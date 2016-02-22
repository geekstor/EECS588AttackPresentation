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

public class CaptchaSpecificMain {
	public String main(String name, int width, int height, int back, int straight, int curved, int shadow, int fish, String filename, String dirname) {
		// TODO Auto-generated method stub
		Captcha captcha = new Captcha.Builder(width, height).build();
		String answer = "";
		while(!answer.equals(name)){
			
				Builder builder = new Captcha.Builder(width, height);
				
				int length = name.length();
				char[] characters = new char[length];
				for(int i = 0; i < length; ++i){
					characters[i] = name.charAt(i);
				}
				
				
				builder.addText(new DefaultTextProducer(length, characters));
				
				
				
				if(back == 0){
					builder.addBackground();
				}
				if(back == 1){
					builder.addBackground(new GradiatedBackgroundProducer());
				}
				if(back == 2){
					builder.addBackground(new SquigglesBackgroundProducer());
				}
				if(curved == 1){
					builder.addNoise(new CurvedLineNoiseProducer());
				}
				if(straight == 1){
					builder.addNoise(new StraightLineNoiseProducer());
				}
				if(fish == 1){
					builder.gimp(new FishEyeGimpyRenderer());
				}
				
				
				
				captcha = builder.build();
				
				answer = captcha.getAnswer();
			
		}
		
		
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
		
			return "";
		
	}
}
