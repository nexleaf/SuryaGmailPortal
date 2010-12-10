'''
Created on Nov 15, 2010

@author: surya
'''
import time
import logging
import os
import traceback

from Logging.Logger import getLog
from Locking.AppLock import getLock

class GmailResultsFramework:
    ''' This class forms the base class for any applications that need to mail results from the database.
    '''
    
    log = getLog("GmailResults")
    
    def __init__(self, level=logging.DEBUG):
        ''' Constructor
        
            Keyword Arguments:
            level -- The logging level.
        '''
        
        self.grestags = ' GMAILRESULTS '
        self.log.setLevel(level)
        
    def checkResults(self):
        ''' Implementors must override this method in order to implement their custom
            result mailing application 
        '''
        
    def run(self, pidfile, programname, timeinterval):
        """ This method runs the danaJob every timeinterval subject to the 
            constraint that if force is True, we process all the images
            that were already processed.
            
            Keyword Arguments:
            pidfile      -- Ensure that only one Application specific dana runs
                            at a time.
            programname  -- Name of the application specific dana.
            timeinterval -- an integer time in seconds after which to repeat dana
        """
        
        if not getLock(pidfile, programname):
            return
        
        while True:
            try:
                self.log.info("Running Gmail Result Mailer", extra=self.grestags)
                self.checkResults()
                self.log.info("Done Running Gmail Result Mailer", extra=self.grestags)
            except Exception, err:
                self.log.critical("Error Checking Results " + str(err) + " :: " + traceback.format_exc(), extra=self.grestags)
            time.sleep(timeinterval)
