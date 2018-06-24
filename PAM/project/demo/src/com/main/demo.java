package com.main;

import cc.mallet.util.*;
import cc.mallet.types.*;
import cc.mallet.pipe.*;
import cc.mallet.pipe.iterator.*;
import cc.mallet.topics.*;

import java.util.*;
import java.util.regex.*;
import java.io.*;
import com.import_chinese.data.*;


public class demo {

	public static void main(String[] args) throws Exception {
	
		import_chinese_data importer = new import_chinese_data();
        InstanceList instances = importer.readDirectory(new File("input/"));

	    
        if(args.length ==0) {
        	System.out.println ("Please enter the -iterationsNum -topWordsNum -superTopicNum -subTopicNum.");
        }else {
        	
    		int numIterations =Integer.parseInt(args[0]);
    		int numTopWords = Integer.parseInt(args[1]);
    		int numSuperTopics = Integer.parseInt(args[2]);
    		int numSubTopics =  Integer.parseInt(args[3]);
    	
    		System.out.println ("Data loaded.");
    		PAM4L pam = new PAM4L (numSuperTopics, numSubTopics);
    		pam.estimate (instances, numIterations, 50, 0, 50, null, new Randoms());  
    		pam.printDocTopWords (new PrintStream("./output/docPercentage-topics.txt"),numTopWords, true);
    		pam.printDoc2Txt (new PrintStream("./output/docPercentage-sub.txt"),0.0,-1,false);
    		pam.printDoc2Txt (new PrintStream("./output/docPercentage-super.txt"),0.0,-1,true);
        }
        
	}

}
