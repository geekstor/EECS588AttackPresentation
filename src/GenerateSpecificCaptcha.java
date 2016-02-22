import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.Random;

public class GenerateSpecificCaptcha {
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		CaptchaSpecificMain generator = new CaptchaSpecificMain();
		
		//int num = Integer.parseInt(args[0]);
		
		String name = args[0];
		
		String baseDir = "captcha-images";
		File theDir = new File(baseDir);
		if (!theDir.exists()) {
			theDir.mkdir();
		}
		
		long timestamp = System.currentTimeMillis();
		File newDir = new File(baseDir + '/' + Long.toString(timestamp));
		if (!newDir.exists()){
			newDir.mkdir();
		}
		
		
		try{
			
			
			
			Random rand = new Random(timestamp % Integer.MAX_VALUE);
			
			int width = 220;
			int height = 52;
			int back = Math.abs(rand.nextInt())%3;
			int straight = Math.abs(rand.nextInt())%2;
			int curved = Math.abs(rand.nextInt())%2;
			int shadow = Math.abs(rand.nextInt())%2;
			int fish = Math.abs(rand.nextInt())%2;
			
			generator.main(name, width, height, back, straight, curved, shadow, fish, 
				Long.toString(timestamp) + '_'
				+ new Integer(1).toString()
				+ ".png",
				baseDir + '/' 
				+ Long.toString(timestamp)
				+'/');
			
			

		}
		catch(Exception e){
			System.out.println("error");
		}
		
	}
}
