from selenium import webdriver
import re
# regular expression to check the validation of url
'''
https://google.com -> valid
https://google.com/abc -> valid
google.com -> not valid
etc..
'''
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE) 

# global variables
# URl : stores the use given url
# window handle : stored the current selenium controlled browser tab

driver,URL,window_handles = None,None,None

#fetch the focusable elements in sequence
def fetch_current_page():
    global window_handles
    window_handles = driver.window_handles
    # switch to the latest opened window
    driver.switch_to.window(window_handles[len(window_handles)-1])
    
    # get the current page title
    #title = driver.execute_script("return document.title")
    page_title = driver.title
    print("Page title: ",page_title)

    # -- java-script
    # get all the focusable elements which are visible in DOM in sequence
    elements = driver.execute_script("""
  
let candidateSelectors = [
    'input',
    'select',
    'textarea',
    'a[href]',
    'button',
    '[tabindex]',
    'audio[controls]',
    'video[controls]',
    '[contenteditable]:not([contenteditable="false"])',
];
let candidateSelector = candidateSelectors.join(',');

let matches =
    typeof Element === 'undefined'
        ? function () { }
        : Element.prototype.matches ||
        Element.prototype.msMatchesSelector ||
        Element.prototype.webkitMatchesSelector;

function tabbable(el, options) {
    options = options || {};

    let regularTabbables = [];
    let orderedTabbables = [];

    let candidates = el.querySelectorAll(candidateSelector);

    if (options.includeContainer) {
        if (matches.call(el, candidateSelector)) {
            candidates = Array.prototype.slice.apply(candidates);
            candidates.unshift(el);
        }
    }

    let candidate;
    let candidateTabindex;
    for (let i = 0; i < candidates.length; i++) {
        candidate = candidates[i];

        if (!isNodeMatchingSelectorTabbable(candidate)) {
            continue;
        }

        candidateTabindex = getTabindex(candidate);
        if (candidateTabindex === 0) {
            regularTabbables.push(candidate);
        } else {
            orderedTabbables.push({
                documentOrder: i,
                tabIndex: candidateTabindex,
                node: candidate,
            });
        }
    }

    let tabbableNodes = orderedTabbables
        .sort(sortOrderedTabbables)
        .map(a => a.node)
        .concat(regularTabbables);

    return tabbableNodes;
}

tabbable.isTabbable = isTabbable;
tabbable.isFocusable = isFocusable;

function isNodeMatchingSelectorTabbable(node) {
    if (
        !isNodeMatchingSelectorFocusable(node) ||
        isNonTabbableRadio(node) ||
        getTabindex(node) < 0
    ) {
        return false;
    }
    return true;
}

function isTabbable(node) {
    if (!node) {
        throw new Error('No node provided');
    }
    if (matches.call(node, candidateSelector) === false) {
        return false;
    }
    return isNodeMatchingSelectorTabbable(node);
}

function isNodeMatchingSelectorFocusable(node) {
    if (node.disabled || isHiddenInput(node) || isHidden(node)) {
        return false;
    }
    return true;
}

let focusableCandidateSelector = candidateSelectors.concat('iframe').join(',');
function isFocusable(node) {
    if (!node) {
        throw new Error('No node provided');
    }
    if (matches.call(node, focusableCandidateSelector) === false) {
        return false;
    }
    return isNodeMatchingSelectorFocusable(node);
}

function getTabindex(node) {
    let tabindexAttr = parseInt(node.getAttribute('tabindex'), 10);
    if (!isNaN(tabindexAttr)) {
        return tabindexAttr;
    }
    // Browsers do not return `tabIndex` correctly for contentEditable nodes;
    // so if they don't have a tabindex attribute specifically set, assume it's 0.
    if (isContentEditable(node)) {
        return 0;
    }
    return node.tabIndex;
}

function sortOrderedTabbables(a, b) {
    return a.tabIndex === b.tabIndex
        ? a.documentOrder - b.documentOrder
        : a.tabIndex - b.tabIndex;
}

function isContentEditable(node) {
    return node.contentEditable === 'true';
}

function isInput(node) {
    return node.tagName === 'INPUT';
}

function isHiddenInput(node) {
    return isInput(node) && node.type === 'hidden';
}

function isRadio(node) {
    return isInput(node) && node.type === 'radio';
}

function isNonTabbableRadio(node) {
    return isRadio(node) && !isTabbableRadio(node);
}

function getCheckedRadio(nodes) {
    for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            return nodes[i];
        }
    }
}

function isTabbableRadio(node) {
    if (!node.name) {
        return true;
    }
    // This won't account for the edge case where you have radio groups with the same
    // in separate forms on the same page.
    let radioSet = node.ownerDocument.querySelectorAll(
        'input[type="radio"][name="' + node.name + '"]'
    );
    let checked = getCheckedRadio(radioSet);
    return !checked || checked === node;
}

function isHidden(node) {
    // offsetParent being null will allow detecting cases where an element is invisible or inside an invisible element,
    // as long as the element does not use position: fixed. For them, their visibility has to be checked directly as well.
    return (
        node.offsetParent === null || getComputedStyle(node).visibility === 'hidden'
    );
}

parent = document.body
const arr = tabbable(parent)
return arr
    """)

    # traverse the array and print in formatted way
    total = len(elements)
    print("total elements ",total)
    data = [] # final array of objects

    for el in range(total):
        # create object for each element
        d = {
#             'page_name':page_title,
#             'id':elements[el].id
            }
        name = elements[el].get_attribute("name")
        text = elements[el].text
        title = elements[el].get_attribute("title")
        value = elements[el].get_attribute("value")
        label = elements[el].get_attribute("aria-label")
        outerHTML = elements[el].get_attribute("outerHTML")
    
        if name:d['element'] = name
        elif text:d['element'] = text
        elif title:d['element'] = title
        elif value:d['element'] = value
        elif label: d['element'] =label
        else:
            d['element'] = "NA" # if no valid identifier found; 
        d['HTML_tag'] = outerHTML
        print(d)
        # push it to the final array of objects
        data.append(d)
        
# program starts here
if __name__ == '__main__':
    isValidURL = False
    # check given url is valid or not
    while not isValidURL:
        URL = input(" Enter the url: ex: https://www.example.com ")
        # url validation
        isValidURL = re.match(regex, URL)
        if not isValidURL:
            print("URL is not valid")

    # if url is valid , go forward 
    print("connecting...")
    
    # driver set up 
    driver = webdriver.Chrome(executable_path=r"C:\Users\Sumax\Desktop\Selenium\chromedriver.exe")
    driver.maximize_window()
    driver.get(URL)
    print("connected; Browse the page...") # connection established

    while True:
        print("1 : to fetch the current page data")
        print("2 : to generate the log file in XLS format")
        print("3 : to quit")
        choice = int(input("Enter your choice"))
        if choice == 1:
            fetch_current_page()
        if choice == 2:
            print("Not implemented in server side")
            pass
            # use data list to generate XLS file
            #generate_log_file()
        if choice == 3:
            print("driver session killed ...")
            driver.quit()
            break
        else:
            print("Enter valid input")   

