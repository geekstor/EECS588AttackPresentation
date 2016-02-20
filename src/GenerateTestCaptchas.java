import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.Random;

public class GenerateTestCaptchas {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		CaptchaMain generator = new CaptchaMain();
		
		//int num = Integer.parseInt(args[0]);
		int num = 100;
		
		String baseDir = "captcha-test-images";
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
			for(int i = 0; i < num; ++i){
				int width = 208;
				int height = 52;
				int back = rand.nextInt()%3;
				int straight = rand.nextInt()%2;
				int curved = rand.nextInt()%2;
				int shadow = rand.nextInt()%2;
				int fish = rand.nextInt()%2;
				

				generator.main(false, width, height, back, straight, curved, shadow, fish, 
						Long.toString(timestamp) + '_'
						+ new Integer(i).toString()
						+ ".png",
						baseDir + '/' 
						+ Long.toString(timestamp)
						+'/');
				
			}
		}
		catch(Exception e){
			System.out.println("error");
		}
	}

}
