def Added(content, event):
    """ Kbtic hooks when add document to lower case tags """
    tags = content.subject
    lowertags = [t.lower() for t in tags]
    content.setSubject(lowertags)
    content.reindexObject()


def Modified(content, event):
    """ Kbtic hooks when edit document to lower case tags """
    tags = content.subject
    lowertags = [t.lower() for t in tags]
    content.setSubject(lowertags)
    content.reindexObject()
