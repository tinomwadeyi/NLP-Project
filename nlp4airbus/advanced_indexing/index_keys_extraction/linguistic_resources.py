"""
Created on 06/06/2018
@author: David ROUSSEL

This is a compilation of various resources (e.g. nltk + scklearn stopwords, fortissimo) that are used by various algorithms. 
They have been centralized in one place to ease maintenance / improvements
"""

stopwords_1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'miss','mr','mrs',
             'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
             'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
             'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
              'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
              'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 
              'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 
              'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 
              'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

stopwords_2 = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", 
                "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "can't", "cannot", "com", "could", "couldn't", 
                "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "else", "ever", "few", "for", "from", "further", 
                "get", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", 
                "herself", "him", "himself", "his", "how", "how's", "http", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", 
                "it's", "its", "itself", "just", "k", "let's", "like", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", 
                "on", "once", "only", "or", "other", "ought", "our", "ours ", "ourselves", "out", "over", "own", "r", "same", "shall", "shan't", "she",
                 "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
                  "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
                   "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've	", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", 
                   "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "www", "you", "you'd", "you'll", "you're", "you've", "your",
                    "yours", "yourself", "yourselves"]

ListStopWords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about',
                 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 
                 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 
                 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 
                 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 
                 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 
                 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 
                 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been',
                 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 
                 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
                 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 
                 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 
                 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than', "iaw", "amm", 
                 "801a", "per", "ref", "add", "utc", 'DAILY','YEAR','DAYS','DAY','MONTHS','MONTH',
                 "JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER",
                'jan', 'feb', 'mar', "apr", "may","jun","jul", "Aug", "sep", "oct", "nov", "dec", 
                 "XXXPLEASE", 'PLEASE','PLZ','THANKS','THANK','SINCE','HRS','HOURS','HOUR']

stopWords = list(set(stopwords_1 + stopwords_2 + ListStopWords))

ListStopWordsUpper = list(map(str.upper, stopWords))

# list of stop words except the ones in prepositional attachment in complex NP
common_in_NP = ["OF", "WITH", "WO", "WITHOUT", "AND", "OR"]
ListStopWordsUpperNotInNP = [x for x in ListStopWordsUpper if x not in common_in_NP]

ListStopWordsUpperNotInNP = '(' + '\\b|\\b'.join(ListStopWordsUpperNotInNP) +')'

# Following list is just an example of word list require to filter out spurious Named entities, 
# often written in uppercase.
# It should be redefined for each project
StopNE = ['ATA','ECAM','MSN','A380','ENG','Main','Entry','Entry Into Service','A380 EIS','AIRBUS','EIS','A380 Entry',
                'A350','A350 Entry','TFU','South', 'North','West','East','Refer','Aircraft',
                'Flight','Test','PFR','CMS','ACMS','Config','Configuration','AFT','SRM','AMM','TSM',
                'AOC','AOG','Maintenance','DO','EVT','snag','analysis',
                'DUE','DEP','BEFORE','AFTER','PRIOR','NEXT','MID','DEPARTURE','PREVIOUS',
                'SOCIAL','SUPPLY','Fault Codes','Fault Code','Fault','Mess','Warning','STDBY','STBY',
                'PN','NFF','NO','SB','deployment']
StopNE = list(map(str.upper, StopNE))

# Fortissimo findings glossary

Findings = [
 'FOLLOWING','CONFIRM','CONFIRMED','OK','SATIS',
 'ITEM','ECAM','SHOW','FOUND','SHOWS','REF','PER',
 'REPORTED', 'SERVICE', 'DEFECTS','NFF','OBSERVED','IMPROVEMENT',
 'COMPLETED','ARRIVED','INITIATED','COMMENCED','STARTED','CLEARED','INFORMED','ADVISED','ACHIEVE','ACHIEVED','OFFERED',
 'ATTACHED','RETURNED','APPLIED','RAISED','WORK','HEAR',
 'DEPARTED','REQUESTED','RECOVERED'
 'ACTION','MAINTENANCE','INVESTIGATION', 'COMMENT','STAFF','REFER','EVEN']


# Fortissimo maintenance actions glossary

Maintenance = ['ADJ','ADJMT','ADJUST','CHECK','CHECK LIST','CHECKLIST','CHK','CND','CYCLED','DAILY CHECK',
 'REMOVED','SET','SWAP','CANCEL','INSTALL','SERVICING','PERFORMED','ADJUSTED','MEL','REPLACE','INSPECTION',
 'REMOVE','RESET','INSTALLED','APPLIED','FILED','CHK','CHECKED','UPDATED','LIMITED',
 'CORRECTED','PROTECTED','USED','ADDED','ADJUST','MAINT','REPLACEMENT',
 'DECTECT','DRAINED','EXCHANG','FINDING','FLUSHED','I/W','INSPECTION','INSPN',
 'INSTALLATION','INTERCHANG','INVESTIG','INVESTIGATION REVEALED','LUB','LUBRIFICATE',
 'LUBRIFY','MISADUJUST','NDT','NO MORE','OBSERVED','OPERATIONAL TEST','ORDERED','POWER UP',
 'PROPER','PROPER INSTALLED','PURGED','R/I','R/R','RR','RACK','REPOSITION','RE-INSTALL',
 'RE-RACK','RE-SECURE','RESTOW','RE-STOW','RE-TIGHT','REACTIVATED','REATTACHED','RECTIF','RECYCLED','REINSTALL','RE-INSTALL',
 'RELOCAT','REMOV','REMOVED AND REPLACED','REMPLACEMENT','REPAIR','REPAIRED','REPAIRING','REPALCE','REPALCED','REPALCEMENT',
 'REPL','REPLAC','REPLD','REPLACED','REPOSITION','RERACK','RE-RACK','RESEAT','RE-SEAT','RESEATED','RESECURE','RESET',
 'RESETS','RESETTING','RESTART','RE-START','RESTOWED','RESURED','RETIGHTENED','REWORK','ROB','ROBBED','RPCLD',
 'RPLCD','RPLCMNT','RPLD','RPLED','SAME C/OUT','SAME CORRECTED','SAME FIXED','SECURE','SUBSTITUTION','SWAP',
 'SWITCHED','SYNCHRON','TEST','TEST/RESET','TGHTD','THAWED','TIGHTEN','TORQUED','TROUBLE-SHOOTING','TROUBLESHOOT',
 'TROUBLESHOOTING','VERIF','WASH']

#Add fortissimo glossaries as antidico
 
Antidico = Findings
 
Antidico.extend(Maintenance)

ListStopWordsOrAntidico = list(set(ListStopWordsUpper + StopNE + Antidico))
