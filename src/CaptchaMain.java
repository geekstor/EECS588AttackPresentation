import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import nl.captcha.Captcha;
import nl.captcha.Captcha.Builder;
import nl.captcha.backgrounds.FlatColorBackgroundProducer;
import nl.captcha.backgrounds.GradiatedBackgroundProducer;
import nl.captcha.backgrounds.SquigglesBackgroundProducer;
import nl.captcha.gimpy.BlockGimpyRenderer;
import nl.captcha.gimpy.DropShadowGimpyRenderer;
import nl.captcha.gimpy.FishEyeGimpyRenderer;
import nl.captcha.gimpy.RippleGimpyRenderer;
import nl.captcha.gimpy.ShearGimpyRenderer;
import nl.captcha.gimpy.StretchGimpyRenderer;
import nl.captcha.noise.CurvedLineNoiseProducer;
import nl.captcha.noise.StraightLineNoiseProducer;
import nl.captcha.text.producer.DefaultTextProducer;

public class CaptchaMain {

	public String main(boolean test, int width, int height, int back, int straight, int curved, int shadow, int fish, String filename, String dirname) {
		// TODO Auto-generated method stub
		Builder builder = new Captcha.Builder(width, height);
		builder.addText(new DefaultTextProducer());

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
