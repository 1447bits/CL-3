import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;


public class ReducerClass extends Reducer<Text, LongWritable, Text, IntWritable> {

	@Override
	protected void reduce(Text key, Iterable<LongWritable> value,Context context)
			throws IOException, InterruptedException {
		int cnt=0;
		for(LongWritable i:value)
		{
			cnt=cnt+1;
		}
		context.write(key, new IntWritable(cnt));
		
	}
}
