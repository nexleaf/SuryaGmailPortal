'''
Created on Nov 15, 2010

@author: surya
'''
import sys
import time
import logging
import os
import traceback

from Logging.Logger import getLog
from Locking.AppLock import getLock

class GmailMonitorFramework:
    ''' This class forms the base class for any applications that intend to poll gmail.
    '''
    
    log = getLog("GmailMonitor")
    gmontags = ' GMAILMONITOR '
                
    def checkInbox(self):
        ''' Implementors must override this method in order to implement their custom
            polling application 
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
                self.log.info("Running Gmail Monitor", extra=self.gmontags)
                self.checkInbox()
                self.log.info("Done Running Gmail Monitor", extra=self.gmontags)
            except Exception, err:
                self.log.critical("Error Checking Inbox " + str(err) + " :: " + traceback.format_exc(), extra=self.gmontags)
            if timeinterval >= 0:
                time.sleep(timeinterval)
            else:
                sys.exit(0)
            
