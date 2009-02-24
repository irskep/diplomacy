import os, re, yaptu, cgi

__rex = re.compile('\s*\<\%([^\<\%]+)\%\>')
__rbe = re.compile('\s*\<\+')
__ren = re.compile('\s*\-\>')
__rco = re.compile('\s*\|= ')

__templater_namespace = locals()

def print_error(error):
    print_template("templates/error_template.html",  locals())

def print_template(template_path, namespace):
    f = open(template_path, 'r')
    s = f.readlines()
    f.close()
    
    #if 'yaptu' not in namespace: namespace.update({'yaptu':yaptu})
    if 'templater' not in namespace: 
        import templater as __templater
        namespace.update({'templater':__templater})
    
    cop = yaptu.copier(__rex, namespace, __rbe, __ren, __rco)
    cop.copy(s)

def print_table(table, table_info, target_page=None, table_name=None, paging=False):
    '''
    Prints a paged html table to the standard out.
        table = a list of lists, tuples, or dicts
        table_info = a tuple or list of the this form
            ((0, "column1"), (3, "column2"), (5, "column3"))
            the numbers refer to the column in the table variable the strings are the name of the
            columns
        target_page = The page the table resides on (needed if paging=True)
        table_name = The name of the table (it doesn't print out just used by the pager to
                     refer to this table, need if paging=True)
        paging = turns paging on or off
    '''
    form = cgi.FieldStorage()
    if form.has_key(table_name+'_page'): page = int(form[table_name+'_page'].value)
    else: page = 0
    
    if paging: rows_per_page = 15
    else: rows_per_page = 0
    
    if (len(table)%rows_per_page) == 0: pages = len(table)/rows_per_page
    else: pages = len(table)/rows_per_page + 1
    
    print_template("templates/create_table.html", locals())

if __name__ == '__main__':
    print locals()
    print globals()
    print dir()
    print __templater_namespace

