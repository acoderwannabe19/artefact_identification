from langserve import RemoteRunnable

artefact_identification = RemoteRunnable("http://localhost:8000/artefact_identification/")

#--------------------------------------------------------------------------------------------------------------------------------
resp = artefact_identification.invoke({"question": "how do i know which user downloaded a file in Windows?"},
                        ) 
print(resp) 

#--------------------------------------------------------------------------------------------------------------------------------
