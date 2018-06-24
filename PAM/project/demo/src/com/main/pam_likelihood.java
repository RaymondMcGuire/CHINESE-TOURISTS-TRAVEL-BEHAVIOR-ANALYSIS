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


public class pam_likelihood {

	public static void main(String[] args) throws Exception {
	
		import_chinese_data importer = new import_chinese_data();
        InstanceList instances = importer.readDirectory(new File("input/"));
        System.out.println ("Data loaded.");
	    
    	
		int numIterations = 1000;
	
		int startSuperNum = 1;
		int endSuperNum =30;
		
		int startSubNum = 1;
		int endSubNum =500;
		
		double maxLikelihood = -999;
		int maxSuperNum = -1;
		int maxSubNum = -1;
	
		for(int sp = startSuperNum;sp<=endSuperNum;sp+=30) {
			for(int sb = startSubNum;sb<=endSubNum;sb+=50) {
				PAM4L pam = new PAM4L (sp, sb);
				double tmpValue =pam.estimate (instances, numIterations, 50, 0, 50, null, new Randoms());  
				if(tmpValue > maxLikelihood) {
					maxLikelihood = tmpValue;
					maxSuperNum = sp;
					maxSubNum = sb;
				}
			}
		}
		
		
	
		System.out.println("max likelihood value:"+maxLikelihood + ",super number:" +maxSuperNum+ ",sub number:" +maxSubNum);
	}

}
