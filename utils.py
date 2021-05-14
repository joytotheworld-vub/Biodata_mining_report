# Extract protein IDs from a FASTA alignment file

badAaCharacters = "X"

def filterSequences(seqAlignments,seqIdList):

  for seqId in seqIdList[:]:

    removed = False
    # Check if has X in it
    for badAaChar in badAaCharacters:
      if seqAlignments[seqId].count(badAaChar):
        print("Removing sequence {}, contains {} character".format(seqId,badAaChar))
        del(seqAlignments[seqId])
        seqIdList.remove(seqId)
        removed = True
        break
                
    # Remove uniref only sequences, won't work
    if not removed:
    
      if seqId.startswith("UniRef90_UPI"):
        print("Removing Uniref sequence {}, does not have uniprot info available".format(seqId))
        seqIdList.remove(seqId)
        del(seqAlignments[seqId])
        
      elif seqId.startswith("UniRef90_"):
        newSeqId = seqId.replace("UniRef90_","")
        seqIdList.insert(seqIdList.index(seqId),newSeqId)
        seqIdList.remove(seqId)
        seqAlignments[newSeqId] = seqAlignments[seqId]
        del(seqAlignments[seqId])
      
  return (seqAlignments,seqIdList)

def extractFastaInfo(fastaAlignment):
  
    """ 
    FASTA file alignment
    """

    # Read the file    
    fin = open(fastaAlignment)
    lines = fin.readlines()
    fin.close()

    startReading = True
    seqAlignments = {}
    seqIdList = []
    
    for line in lines:        

      cols = line.split()

      if cols:
      
        if cols[0].startswith('>'):
          seqId = cols[0][1:].strip()
          seqIdList.append(seqId)

        else:
          if seqId not in seqAlignments.keys():
            seqAlignments[seqId] = cols[0].upper()
          else:
            # Multiline FASTA
            seqAlignments[seqId] += cols[0].upper()
            
    filterSequences(seqAlignments, seqIdList)

    return (seqAlignments, seqIdList)
    
# Extract protein IDs from a CLUSTAL alignment file
def extractClustalInfo(clustalAlignment,uniqueSeqs=False):
    
    """
    CLUSTAL files

    If uniqueSeqs is True, will add extra suffix to overlapping identifiers occuring more than once, so they end up separately
    """
    # Read the file    
    fin = open(clustalAlignment)
    lines = fin.readlines()
    fin.close()
        
    startReading = False
    seqAlignments = {}
    seqIdList = []

    for line in lines:
      
      if line.startswith("CLUSTAL"):
        startReading = True
        continue
        
      if startReading:
        cols = line.split()
        
        if cols:          
          if len(cols) in (2,3):

            # Ignore lines with annotation information
            if cols[0][0].count('*') or cols[0][0].count(":") or cols[0].isdigit():
              continue
  
            seqId = cols[0].split("|")[1]

            if uniqueSeqs and seqId in seqAlignments.keys():
              for i in range(99):
                newSeqId = "{}_{}".format(seqId,i)
                if newSeqId not in seqAlignments.keys():
                  seqId = newSeqId
                  break
            
            alignment = cols[1]
            
            if seqId not in seqAlignments.keys():
              seqAlignments[seqId] = ""
              seqIdList.append(seqId)
            
            seqAlignments[seqId] += alignment

    filterSequences(seqAlignments, seqIdList)

    return (seqAlignments, seqIdList)



