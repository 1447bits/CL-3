import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;




public class MapperClass extends Mapper<LongWritable, Text, Text, LongWritable>{
	@Override
	protected void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {
		
		String w[] =value.toString().split(" ");
		for (String word:w)
		{
			context.write(new Text(word), new LongWritable(1));
			
		}
		
	}
	
	
}
