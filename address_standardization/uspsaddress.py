"""
Author: Sou-Cheng Choi
Contributor: Jack Huang
Date: May 27, 2016 -- Aug 3, 2017
Reference: Choi, Sou-Cheng T., Yongheng Lin, and Edward Mulrow.
"Comparison of Public-Domain Software and Services for Probabilistic Record Linkage and Address Standardization,"
Towards Integrative Machine Learning and Knowledge Extraction, Springer LNAI 10344, 2017.
PDF available at http://tinyurl.com/ydxbjww4
"""
import csv
import googlemaps
import time # for sleep()
import usaddress

"""
from uspsaddress import uspsaddress
usadd = uspsaddress()
usadd.eval_googlemaps()

"""

class uspsaddress(object):
    isverbose = True

    usaddress_sleep = 0

    time_stamp = time.time()

    log_file = open("uspsaddress"+str(time_stamp)+".log", "w");

    usps_headers = ['street_num', 'street_pre_dir', 'street_name', 'street_suffix', 'street_post_dir',
                    'unit_type', 'unit_num', 'city', 'state_abbrev', 'zip', 'zip4']

    usps_po_box_headers = ['street_pre_dir', 'street_name', 'street_num', 'street_suffix',  'street_post_dir',
                           'unit_type', 'unit_num', 'city', 'state_abbrev', 'zip', 'zip4']

    googlemaps_headers = ['street_number', 'route', 'locality', 'administrative_area_level_1', 'postal_code',
                          'postal_code_suffix']

    headers_googlemaps2usps = {'postal_code':'zip', 'postal_code_suffix':'zip4','locality':'city',
                                 'administrative_area_level_1':'state_abbrev', 'street_number':'street_num',
                                 'subpremise':'unit_num'}


    headers_usaddress2usps = {'ZipCode':'zip', 'ZipPlus4':'zip4','PlaceName':'city',
                                 'StreetNamePreDirectional':'street_pre_dir', 'StateName':'state_abbrev',
                                 'StreetNamePostDirectional': 'street_post_dir',
                                 'USPSBoxID':'street_num', 'AddressNumber':'street_num',
                                 'USPSBoxType':'street_name', 'StreetName':'street_name',
                                 'StreetNamePostType':'street_suffix',
                                 'OccupancyType':'unit_type','OccupancyIdentifier':'unit_num'}

    def __init__(self):
        """
        Constructor

        >>> from uspsaddress import uspsaddress
        >>> usadd = uspsaddress()
        """
        if self.isverbose:
            print >> self.log_file, "In 'uspsaddress' class"


    def print_record(self, row):
        """

        >>> from uspsaddress import uspsaddress
        >>> usadd = uspsaddress()
        >>> s = usadd.print_record({'street_num': "55", 'street_pre_dir': "N"})
        street_num : 55
        street_pre_dir : N
        <BLANKLINE>
        """
        if self.isverbose==False:
            return

        s = ""
        for k,v in row.iteritems():
            if len(v) > 0:
                s += (  k + " : " + str(v) + "\n" )
        return s


    def map_googlemaps_result(self, row2, header2, value2):
        """
        >>> 1 + 1
        2

        """

        row2[self.headers_googlemaps2usps[header2]] = value2

        """
        if header2 == 'postal_code':
            row2['zip'] = value2
        elif header2 == 'postal_code_suffix':
            row2['zip4'] = value2
        elif header2 == 'locality':
            row2['city'] = value2
        elif header2 == 'administrative_area_level_1':
            row2['state_abbrev'] = value2[0:2]
        elif header2 == 'street_number':
            row2['street_num'] = value2
        elif header2 == 'subpremise':
            row2['unit_num'] = value2
        el
        """
        if header2 == 'route':
            s = value2.split()
            s_len = len(s)
            idx = s_len - 1
            if s[0].uppper() in ["NORTH", "SOUTH","EAST","WEST"]:
                row2['street_pre_dir'] = s[0][0]
                row2['street_name'] = " ".join(s[1:idx])
            else:
                row2['street_name'] = " ".join(s[0:idx])

            row2['street_suffix'] = s[idx][0:2]
            if s[idx].upper() == "ROAD":
                row2['street_suffix'] = "RD"
            elif s[idx].upper() == "LANE":
                row2['street_suffix'] = "LN"
            elif s[idx].upper() == "AV":
                row2['street_suffix'] = "AVE"

    def map_usaddress_result(self, result):
        # self.map_usaddress_record(result)
        row2 = {}
        for h in self.usps_headers:
            row2[h] = ""

        for elmt in result:
            header2 = elmt[1]
            value2 = elmt[0]
            if not(header2 in ['PlaceName', 'USPSBoxType', 'StreetName','OccupancyIdentifier']):
                if not header2 in self.headers_usaddress2usps.keys():
                    print >> self.log_file, "ERROR: ", header2, " not in headers_usaddress2usps"
                    #TODO Follow up on fields such as 'AddressNumberSuffix'
                    continue

                usps_header = self.headers_usaddress2usps[header2]
                row2[usps_header] = value2
            elif header2 == 'PlaceName':
                    row2['city'] += (" " + value2)
                    row2['city'] = row2['city'].strip()
            elif header2 in ['USPSBoxType', 'StreetName']:
                row2['street_name'] += (" " + value2)
                row2['street_name'] = row2['street_name'].strip()
            elif header2 in ['OccupancyIdentifier']:
                if row2['unit_num'] == "":
                    row2['unit_num'] = value2
                else:
                    row2['unit_num'] = [row2['unit_num'], value2]

        print >> self.log_file, "Mapped result:\n", row2, "\n"
        s = self.print_record(row2)
        if self.isverbose:
            print >> self.log_file, s
        return row2


    def compare2records(self, row1, row2, wrong_counts, right_counts):
        right_count = 0.0
        count = 0

        for (h,v) in row1.iteritems():
            count += 1

            if not isinstance(row2[h], list):
                #print row2[h], len(row2[h])
                if v.upper() == row2[h].upper():
                    val = 1.0
                    right_counts[h] += val
                    right_count += val
                else:
                    if self.isverbose:
                        print >> self.log_file, "Mismatched field: ", h, ". Values: usps : ", v, ", parsed : ", row2[h]
                    wrong_counts[h] += 1
            else:
                for elmt in row2[h]:
                    if v.upper() == elmt:
                        val = (1.0/len(row2[h]))
                        right_counts[h] += val
                        right_count += val
                        continue
                    else:
                        if self.isverbose:
                            print >> self.log_file, "Mismatched field: ", h, ". Values: usps : ", v, ", parsed : ", str(row2[h])
                wrong_counts[h] += (1.0 - (1.0/len(row2[h])))

        wrong_count = count - right_count

        if self.isverbose:
             print >> self.log_file, "\nRight and wrong counts:", right_count, wrong_count
             if (right_count + wrong_count) > 0:
                 accuracy = right_count * 1.0/ (right_count+wrong_count)
                 print >> self.log_file, "\nAccuracy:", accuracy
                 if accuracy < 1.0:
                     print >> self.log_file, "***REVIEW***"

        return right_count, wrong_count, wrong_counts


    def usps_csv_row2_dict_and_address_line(self, row):
        row1 = {}
        address_line = ""

        if row['street_name'].upper() == "PO BOX":
            for h in self.usps_po_box_headers:
                if len(row[h].strip()) > 0:
                    address_line += (row[h] + " ")
                    row1[h] = row[h]
        else:
            for h in self.usps_headers:
                if len(row[h].strip()) > 0:
                    address_line += (row[h] + " ")
                    row1[h] = row[h]

        if self.isverbose:
            s = self.print_record(row1)
            print >> self.log_file, s, "\nInput address line:", address_line,"\n"

        return address_line, row1


    def usaddress_parse_address_line(self, address_line="", wrong_counts={}):
        ifsuccess = False
        result = {}
        if address_line=="":
            wrong_counts['no_input'] += 1
            return ifsuccess, result, wrong_counts

        try:
            result = usaddress.parse(address_line)
            ifsuccess = True
            time.sleep(self.usaddress_sleep)
        except:
            print >> self.log_file, "ERROR: usaddress timeout"
            wrong_counts['timeout'] += 1
            return ifsuccess, result, wrong_counts

        if len(result) == 0:
            msg = " ".join(["ERROR: len(geocode_result) == 0", address_line, "\n"])
            print >> self.log_file, msg

        if self.isverbose:
            print >> self.log_file, "Parsed result:\n",result,"\n"

        return ifsuccess, result, wrong_counts


    def update_counts(self, total_right_count, total_wrong_count, right_count, wrong_count, id):
        total_wrong_count += wrong_count
        total_right_count += right_count
        total_counts = total_right_count + total_wrong_count
        if total_counts > 0:
            accuracy = total_right_count * 1.0 / (total_right_count + total_wrong_count)

        s = "****" + ", ".join([str(id), str(right_count), str(wrong_count), str(total_right_count), str(total_wrong_count), str(accuracy)])

        if self.isverbose:
            print >> self.log_file,  s

        print s

        return total_right_count, total_wrong_count


    def initalize_counts_dict(self):
        wrong_counts = {}
        for h in self.usps_headers:
            wrong_counts[h] = 0
        wrong_counts['timeout'] = 0
        wrong_counts['no_input'] = 0
        #print wrong_counts
        return wrong_counts


    def print_counts(self, wrong_counts, right_counts):
        wrong_counts_str = "".join(["wrong counts: \n", str(wrong_counts)])
        print >> self.log_file, wrong_counts_str
        print wrong_counts_str

        right_counts_str = "".join(["right counts: \n", str(right_counts)])
        print >> self.log_file, right_counts_str
        print right_counts_str


    def eval_usaddress(self, n=20000):
        """
        162 PENDEXTER AVE CHICOPEE MA 01013 2126
        216 E HILL RD BRIMFIELD MA 01010 9799


        >>> from uspsaddress import uspsaddress
        >>> usadd = uspsaddress()
        >>> usadd.eval_usaddress(1)
        ****1, 6.0, 0.0, 6.0, 0.0, 1.0
        wrong counts:
        {'city': 0, 'unit_num': 0, 'no_input': 0, 'street_post_dir': 0, 'zip': 0, 'street_name': 0, 'street_pre_dir': 0, 'street_suffix': 0, 'unit_type': 0, 'state_abbrev': 0, 'timeout': 0, 'street_num': 0, 'zip4': 0}

        """

        inputfile = "../../Data/samplefordatalinkage.csv"
        #inputfile =  "../../Data/test.csv"
        wrong_counts = self.initalize_counts_dict()
        right_counts = self.initalize_counts_dict()
        total_wrong_count = 0
        total_right_count = 0
        row_count = 0

        if self.isverbose:
            print >> self.log_file, "In eval_usaddress: n = ", str(n)

        with open(inputfile, "rb") as f:
            reader = csv.DictReader(f);
            for row in reader:
                row_count += 1
                if row_count <= n:
                    if self.isverbose:
                        print >> self.log_file, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", row_count
                else:
                    break

                address_line, row1 = self.usps_csv_row2_dict_and_address_line(row)
                ifsuccess, result, wrong_counts = self.usaddress_parse_address_line(address_line, wrong_counts)
                if not ifsuccess:
                    continue
                row2 = self.map_usaddress_result(result)
                right_count, wrong_count, wrong_counts = self.compare2records(row1, row2, wrong_counts, right_counts)
                total_right_count, total_wrong_count = self.update_counts(total_right_count, total_wrong_count,
                                                                          right_count, wrong_count, row_count)

        self.print_counts(wrong_counts, right_counts)

        f.close()



    def eval_googlemaps(self, n=20000):

        """
        162 PENDEXTER AVE CHICOPEE MA 01013 2126
        216 E HILL RD BRIMFIELD MA 01010 9799


        >> from uspsaddress import uspsaddress
        >> usadd = uspsaddress()
        >> usadd.eval_googlemaps(1)
        3 3
        0.5

        """
        # g = open("../../Data/x.txt", "w");
        wrong_counts = {}
        for h in self.usps_headers:
            wrong_counts['h'] = 0
        wrong_counts['timeout'] = 0

        total_wrong_count = 0
        total_right_count = 0
        row_count = 0
        #gmaps = googlemaps.Client(key='AIzaSyBOit9CjPZ7KB_sDtKYxz6UN7qr-RRxZ1k')
        gmaps = googlemaps.Client(key='AIzaSyDs50RAAd4Bwh - x9WPM5hj68wnuA1tv - Uk')
        with open("../../Data/samplefordatalinkage.csv", "rb") as f:
            reader = csv.DictReader(f);
            for row in reader:
                wrong_count = 0
                right_count = 0
                row_count += 1
                if row_count <= n:
                    if self.isverbose:
                        print >> self.log_file, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", row_count
                else:
                    break

                row1 = {}
                # create one-line address without commas
                address_line = ""

                if row['street_name'].upper() == "PO BOX":
                    for h in self.usps_po_box_headers:
                        if len(row[h].strip()) > 0:
                            address_line += (row[h] + " ")
                        row1[h] = row[h]
                        wrong_counts[h] = 0
                else:
                    for h in self.usps_headers:
                        if len(row[h].strip()) > 0:
                            address_line += (row[h] + " ")
                        row1[h] = row[h]
                        wrong_counts[h] = 0


                if self.isverbose:
                    s = self.print_record(row1)
                    print >> self.log_file, s, address_line,"\n"

                try:
                    geocode_result = gmaps.geocode(address_line)
                    time.sleep(2)
                except googlemaps.exceptions.Timeout:
                    print >> self.log_file, "ERROR: googlemaps timeout"
                    wrong_counts['timeout'] += 1
                    continue


                if len(geocode_result) == 0:
                    print >> self.log_file, "ERROR: len(geocode_result) == 0", address_line,"\n"
                    continue

                if self.isverbose:
                    print >> self.log_file, geocode_result

                row2 = {}
                for h in self.usps_headers:
                    row2[h] = ""

                for i in range(len(geocode_result[0]['address_components'])):
                    header2 = geocode_result[0]['address_components'][i]['types'][0].strip()
                    value2 = geocode_result[0]['address_components'][i]['short_name'].strip()
                    if self.isverbose:
                        print >> self.log_file, header2, ":", value2

                    self.map_googlemaps_result(row2, header2, value2)

                s = self.print_record(row2)
                if self.isverbose:
                    print >> self.log_file, s

                right_count, wrong_count = self.compare2records(row1, row2)
                total_right_count += right_count
                total_wrong_count += wrong_count

                if self.isverbose:
                    print >> self.log_file, right_count, wrong_count
                    if (right_count + wrong_count) > 0:
                        print >> self.log_file,  right_count * 1.0/ (right_count+wrong_count)


        print >> self.log_file, total_right_count, total_wrong_count
        print total_right_count, total_wrong_count
        if (total_right_count+total_wrong_count) > 0:
            print >> self.log_file,  total_right_count * 1.0/ (total_right_count+total_wrong_count)
            print total_right_count * 1.0/ (total_right_count+total_wrong_count)
        f.close()  # g.close()


if __name__=='__main__':
    # python uspsaddress.py -v
    # Or:
    # python uspsaddress.py
    import doctest, uspsaddress
    doctest.testmod(uspsaddress)
