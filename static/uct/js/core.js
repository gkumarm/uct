// Core javascript helper functions of uct

// basic browser identification & version
var isOpera = (navigator.userAgent.indexOf("Opera") >= 0) && parseFloat(navigator.appVersion);
var isIE = ((document.all) && (!isOpera)) && parseFloat(navigator.appVersion.split("MSIE ")[1].split(";")[0]);

// ----------------------------------------------------------------------------
// Generic Implementation for GET Submit action
// ----------------------------------------------------------------------------
function getActionButtonClicked (form, action, next) 
{
    // Uncomment if needed for remembering pagination location
    // var navList = document.getElementById ("navTo");
    // if(navList.length > 0)
    //     document.form1.listpageid.value = navList [navList.selectedIndex].value;
    // else
    //     document.form1.listpageid.value = 1;
    if (action == 'crudCreate' || action=='Filter') {
        form.action.value = action;
        form.submit();
        return;
    } else {
        var control = form.pk_radio;
        if (control != null)  {
            if(control.length != null) {
                for(var i = 0; i < control.length; i++) {
                    if(control[i].checked) {
                        form.action = action.replace('999', control[i].value) + next;
                        form.method = "GET";
                        form.submit();
                        return;
                    }
                }
            } else {
                if(control.checked) {
                    form.action = action.replace('999',control.value) + next;
                    form.method = "GET";
                    form.submit();
                    return;
                }
            }
        }
    } 
    alert ('No record selected.');
}

function hmAction (action, loc) 
{
    var x = document.getElementById("id_from_date");
    if (x.value == '') {
        return;
    } else {
        if (action == 'prev') {
            location = loc + '?start_date=' + x.value + '&offset=-30';
        } else if (action == 'next') {
            location = loc + '?start_date=' + x.value + '&offset=30';
        } else if (action == 'today') {
            location = loc;
        } else if (action == 'option') {
            location = loc + '?start_date=' + x.value + '&offset=0';
        }        
    }
}
