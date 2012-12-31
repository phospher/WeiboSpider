def importClass(classFullname):
    moduleName, className = classFullname.rsplit('.', 1)
    module=__import__(moduleName)
    return module.getattr(module, className)
