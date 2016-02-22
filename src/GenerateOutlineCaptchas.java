import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.Random;

public class GenerateOutlineCaptchas {
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		CaptchaOutlineMain generator = new CaptchaOutlineMain();
		
		//int num = Integer.parseInt(args[0]);
		int num = 100;
		
		String answer = "";
		
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
			File answers = new File(baseDir + '/' 
					+ Long.toString(timestamp) + '/' 
					+ "control.txt");
			if(!answers.exists()){
				answers.createNewFile();
			}
			
			FileWriter fw = new FileWriter(answers.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);
			
			
			Random rand = new Random(timestamp % Integer.MAX_VALUE);
			for(int i = 0; i < num; ++i){
				int length = Math.abs(rand.nextInt())%4 + 5;
				int width = 220;
				int height = 52;
				int back = Math.abs(rand.nextInt())%2;
				int straight = Math.abs(rand.nextInt())%2;
				int curved = Math.abs(rand.nextInt())%2;
				int shadow = Math.abs(rand.nextInt())%2;
				

				answer = generator.main(false, length, width, height, back, straight, curved, shadow, 
						Long.toString(timestamp) + '_'
						+ new Integer(i).toString()
						+ ".png",
						baseDir + '/' 
						+ Long.toString(timestamp)
						+'/');
				
				bw.write(answer);
				bw.newLine();
			}

			bw.close();
		}
		catch(Exception e){
			System.out.println("error");
		}
		
	}
}
