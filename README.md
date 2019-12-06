# RowSheet API Manager.

Add this to your `.vimrc` to get syntax highlighting for the API spec `yaml` files!

    " API Spec Syntax

    fun! RS_APISpec_Syntax()

        " spec keys (version, service, module, method, params)
        syn match rsh_version /\%(version:\)/
        hi def rsh_version ctermfg=214 ctermbg=NONE cterm=bold
        syn match rsh_services /\%(services:\)/
        hi def rsh_services ctermfg=214 ctermbg=NONE cterm=bold
        syn match rsh_methods /\%(methods:\)/
        hi def rsh_methods ctermfg=214 ctermbg=NONE cterm=bold
        syn match rsh_modules /\%(modules:\)/
        hi def rsh_modules ctermfg=214 ctermbg=NONE cterm=bold
        syn match rsh_params /\%(params:\)/
        hi def rsh_params ctermfg=214 ctermbg=NONE cterm=bold

        " methods attributes (method, args, type, optional)
        syn match rsh_type /\%(type:\)/
        hi def rsh_type ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_method /\%(method:\)/
        hi def rsh_method ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_args /\%(args:\)/
        hi def rsh_args ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_optional /\%(optional:\)/
        hi def rsh_optional ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_auth /\%(auth:\)/
        hi def rsh_auth ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_required /\%(required:\)/
        hi def rsh_required ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_default /\%(default:\)/
        hi def rsh_default ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_min /\%(min:\)/
        hi def rsh_min ctermfg=75 ctermbg=NONE cterm=bold
        syn match rsh_max /\%(max:\)/
        hi def rsh_max ctermfg=75 ctermbg=NONE cterm=bold

        " documentation data.
        syn match rsh_description /\%(description:\)/
        hi def rsh_description ctermfg=112 ctermbg=NONE cterm=bold

        " enums (POST, GET, DELETE)
        syn match rsh_post /\%(POST\)/
        hi def rsh_post ctermfg=219 ctermbg=NONE cterm=bold
        syn match rsh_get /\%(GET\)/
        hi def rsh_get ctermfg=219 ctermbg=NONE cterm=bold
        syn match rsh_delete /\%(DELETE\)/
        hi def rsh_delete ctermfg=219 ctermbg=NONE cterm=bold

        " todo
        syn match rsh_todo /\%(status: todo\)/
        hi def rsh_todo ctermfg=196 ctermbg=NONE cterm=bold
        syn match rsh_beta /\%(status: beta\)/
        hi def rsh_beta ctermfg=196 ctermbg=NONE cterm=bold
    endfu

    autocmd bufenter * :call RS_APISpec_Syntax()
    autocmd filetype * :call RS_APISpec_Syntax()

# Legal

> © 2019-present, Alexander Kleinhans  
> All Rights Reserved  

## By RowSheet, LLC

> Company:    RowSheet, LLC  
> Contact:    alex@rowsheet.com  
> Website:  [rowsheet.com](https://rowsheet.com/)  
> Address:    312 Cheyenne St. Denver, CO 80403  
> [Github](https://github.com/rowsheet)  
