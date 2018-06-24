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


public class HPAM_demo {

	public static void main(String[] args) throws Exception {
	
		import_chinese_data importer = new import_chinese_data();
        InstanceList instances = importer.readDirectory(new File("input/"));
        InstanceList testing = null;
	    
    	
		int numIterations = 1000;
		int numTopWords = 15;
		int numSuperTopics = 5;
		int numSubTopics = 15;
	
		System.out.println ("Data loaded.");
		
		

      

		HierarchicalPAM pam = new HierarchicalPAM (numSuperTopics, numSubTopics,1, 1);
		pam.estimate (instances, testing, numIterations, 100, 0, 250, null, new Randoms());
		
//		PAM4L pam = new PAM4L (numSuperTopics, numSubTopics);
//		pam.estimate (instances, numIterations, 50, 0, 50, null, new Randoms());  
//		pam.printDocTopWords (new PrintStream("./output/docPercentage-topics.txt"),numTopWords, true);
//		pam.printDoc2Txt (new PrintStream("./output/docPercentage-sub.txt"),0.0,-1,false);
//		pam.printDoc2Txt (new PrintStream("./output/docPercentage-super.txt"),0.0,-1,true);
        
        
	}

}
