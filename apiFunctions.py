import os
import requests

def downloadFile(url,fileName):
    """
    Downloads a file from the internet with a given url.
    The function delete any existing files with the given filename.
    It will then download and name the new file.
    The function is designed to also work with very big files.
    
    Parameters
    ----------
    url : str
        url that is needed used to download a file.
    fileName : str
        Name of the new file
    
    Returns
    -------
    fileName : str
        returns the name of the new file
    """
    # Delete existing files with filename
    try:
        os.remove(fileName) 
    except:
        pass
    
    """ Use requests to download file. 
    Works with streams to be able large files without having the need of a 
    large memory.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)
    return fileName

def uniprotDownload(fileName, query="",format="list",columns="",include="no",compress="no",limit=0,offset=0):
    """Downloads file from uniprot for given parameters
    
    If no parameters are given the function will download a list of all the 
    proteins ID's. More information about how the URL should be constructed can
    be found on: 
    https://www.uniprot.org/help/api%5Fqueries
    
    Parameters
    ----------
    fileName : str
        name for the downloaded file
    query : str (Default='')
        query that would be searched if as you used the webinterface on 
        https://www.uniprot.org/. If no query is provided, all protein entries
        are selected. 
    format : str (Default='list')
        File format you want to retrieve from uniprot. Available format are:
        html | tab | xls | fasta | gff | txt | xml | rdf | list | rss
    columns : str (Default='')
        Column information you want to know for each entry in the query 
        when format tab or xls is selected.
    include : str (Default='no')
        Include isoform sequences when the format parameter is set to fasta.
        Include description of referenced data when the format parameter is set to rdf.
        This parameter is ignored for all other values of the format parameter.
    compress : str (Default='no')
        download file in gzipped compression format.
    limit : int (Default=0)
        Limit the amount of results that is given. 0 means you download all.
    offset : int (Default=0)
        When you limit the amount of results, offset determines where to start.
        
    Returns
    -------
    fileName : str
        Name of the downloaeded file.
    """
    def generateURL(baseURL, query="",format="list",columns="",include="no",compress="no",limit="0",offset="0"):
        """Generate URL with given parameters"""
        def glueParameters(**kwargs):
            gluedParameters = ""
            for parameter, value in kwargs.items():
                gluedParameters+=parameter + "=" + str(value) + "&"
            return gluedParameters.replace(" ","+")[:-1] #Last "&" is removed, spacec replaced by "+"
        return baseURL + glueParameters(query=query,
                                        format=format,
                                        columns=columns,
                                        include=include,
                                        compress=compress,
                                        limit=limit,
                                        offset=offset)
    URL = generateURL("https://www.uniprot.org/uniprot/?",
               query=query,
               format=format,
               columns=columns,
               include=include,
               compress=compress,
               limit=limit,
               offset=offset)
    return downloadFile(URL, fileName)

def enaDownload(fileName, accession, format="fasta"):
    url = "https://www.ebi.ac.uk/ena/data/view/{0}&display={1}".format("AE004091","fasta")
    return downloadFile(url, fileName)