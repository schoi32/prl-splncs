/**
* Author: Sou-Cheng Choi
* Date: May 27, 2016 -- Aug 3, 2017
* Reference: Choi, Sou-Cheng T., Yongheng Lin, and Edward Mulrow. "Comparison of Public-Domain Software and Services for Probabilistic Record Linkage and Address Standardization,” Towards Integrative Machine Learning and Knowledge Extraction, Springer LNAI 10344, 2017. To appear. PDF available at http://tinyurl.com/ydxbjww4
*/
package serf.data;

import java.util.Properties;

/**
 * 
 * Use this class to compare Record objects containing yahoo shopping data.
 * Specifically these records should contain the following attributes:
 * 
 * price - the price of the item being sold
 * title - the title of the item being sold
 *
 * Note: this class is similar to YahooMatcherMerger. It works with serialized records of a slightly different format.
 * 
 */
public class RLdataMatcherMerger extends BasicMatcherMerger implements
		MatcherMerger {

	PriceMatcher yearMatcher;
	PriceMatcher monthMatcher;
	PriceMatcher dayMatcher;
	TitleMatcher lnameMatcher;
	TitleMatcher fnameMatcher;
	TitleMatcher lname2Matcher;
	TitleMatcher fname2Matcher;

	public RLdataMatcherMerger(Properties props)
	{
		_factory = new SimpleRecordFactory();
		
		//The following property strings are from .conf file:
		String tt  = props.getProperty("LnameThreshold");
		String tt2 = props.getProperty("FnameThreshold");
		String ttb  = props.getProperty("Lname2Threshold");
		String tt2b = props.getProperty("Fname2Threshold");
		String pt  = props.getProperty("YearThreshold");
		String pt2  = props.getProperty("MonthThreshold");
		String pt3  = props.getProperty("DayThreshold");
		
		//TODO change the following to double
		float tf  = tt == null ? 0.9F : Float.parseFloat(tt);
		float tf2 = tt2 == null ? 0.9F : Float.parseFloat(tt2);
		float tfb  = ttb == null ? 0.9F : Float.parseFloat(ttb);
		float tf2b = tt2b == null ? 0.9F : Float.parseFloat(tt2b);
		float pf  = pt == null ? 0.33F : Float.parseFloat(pt);
		float pf2  = pt2 == null ? 0.33F : Float.parseFloat(pt2);
		float pf3  = pt3 == null ? 0.33F : Float.parseFloat(pt3);
		
		lnameMatcher  = new TitleMatcher(tf);
		fnameMatcher = new TitleMatcher(tf2);
		lname2Matcher  = new TitleMatcher(tfb);
		fname2Matcher = new TitleMatcher(tf2b);
		yearMatcher  = new PriceMatcher(pf);
		monthMatcher  = new PriceMatcher(pf2);
		dayMatcher  = new PriceMatcher(pf3);
		
	}
	
	protected double calculateConfidence(double c1, double c2)
	{
		return 1.0;
	}
	
	public RLdataMatcherMerger(RecordFactory factory) 
	{
		_factory = factory;
		lnameMatcher = new TitleMatcher(0.9F);
		fnameMatcher = new TitleMatcher(0.9F);
		lname2Matcher = new TitleMatcher(0.9F);
		fname2Matcher = new TitleMatcher(0.9F);
		yearMatcher  = new PriceMatcher(0.33F);
		monthMatcher = new PriceMatcher(0.33F);
		dayMatcher  = new PriceMatcher(0.33F);
	}

	public RLdataMatcherMerger(RecordFactory factory, float tt, float tt2, float ttb, float tt2b, float pt, float pt2, float pt3) {
		_factory = factory;
		lnameMatcher = new TitleMatcher(tt);
		fnameMatcher = new TitleMatcher(tt2);
		lname2Matcher = new TitleMatcher(ttb);
		fname2Matcher = new TitleMatcher(tt2b);
		yearMatcher  = new PriceMatcher(pt);
		monthMatcher = new PriceMatcher(pt2);
		dayMatcher  = new PriceMatcher(pt3);
	}
	
	protected boolean matchInternal(Record r1, Record r2)
	{
		
		//ExistentialBooleanComparator equals = new ExistentialBooleanComparator(new EqualityMatcher());

		Attribute p1 = r1.getAttribute("by");
		Attribute p2 = r2.getAttribute("by");
		if (!ExistentialBooleanComparator.attributesMatch(p1, p2, yearMatcher))
			return false;

		Attribute m1 = r1.getAttribute("bm");
		Attribute m2 = r2.getAttribute("bm");
		if (!ExistentialBooleanComparator.attributesMatch(m1, m2, monthMatcher))
			return false;
		
		Attribute d1 = r1.getAttribute("bd");
		Attribute d2 = r2.getAttribute("bd");
		if (!ExistentialBooleanComparator.attributesMatch(d1, d2, dayMatcher))
			return false;

		Attribute t1 = r1.getAttribute("lname_c1");
		Attribute t2 = r2.getAttribute("lname_c1");	
		if (!ExistentialBooleanComparator.attributesMatch(t1, t2, lnameMatcher))
			return false;
		
		Attribute t1b = r1.getAttribute("lname_c2");
		Attribute t2b = r2.getAttribute("lname_c2");	
		if (!ExistentialBooleanComparator.attributesMatch(t1b, t2b, lname2Matcher))
			return false;
		
		Attribute s1 = r1.getAttribute("fname_c1");
		Attribute s2 = r2.getAttribute("fname_c1");
		if (!ExistentialBooleanComparator.attributesMatch(s1, s2, fnameMatcher))
			return false;
		
		Attribute s1b = r1.getAttribute("fname_c2");
		Attribute s2b = r2.getAttribute("fname_c2");	
		return ExistentialBooleanComparator.attributesMatch(s1b, s2b, fname2Matcher);
	}

}
