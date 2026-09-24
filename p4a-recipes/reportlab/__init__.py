from pythonforandroid.recipe import PythonRecipe, IncludedFilesBehaviour

class ReportLabRecipe(IncludedFilesBehaviour, PythonRecipe):
    """
    ReportLab fourni localement afin d'éviter le téléchargement
    depuis hg.reportlab.com, qui retourne HTTP 403 dans GitHub Actions.
    """
    
    version = "fe660f227cac"
    
    # Aucun téléchargement Internet.
    url = None
    
    # Archive présente directement dans le dépôt GitHub.
    src_filename = "reportlab-fe660f227cac.tar.gz"
    
    depends = ["python3"]
    
    site_packages_name = "reportlab"
    
    
    recipe = ReportLabRecipe()
