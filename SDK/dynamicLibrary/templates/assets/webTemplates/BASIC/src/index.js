import Furhat from 'furhat-core'
import FurhatGUI from 'furhat-gui'

FurhatGUI(function(furhat) {
    furhat.subscribe('furhatos.event.responses.ResponseSkillGUIName', function(data) {
        if(data.port == window.location.port) {
            setPageTitle(data.name)
        }
    })
    
    furhat.subscribe('furhatos.event.actions.ActionSkillGUIClear', function(data) {
        if(data.port == window.location.port) {
            clearScreen()
        }
    })
    
    furhat.subscribe('furhatos.event.actions.ActionSkillGUIWrite', function(data) {
        if(data.port == window.location.port) {
            clearScreen()
            appendText(data.text)
        }
    })
    
    furhat.subscribe('furhatos.event.actions.ActionSkillGUIAppend', function(data) {            
        if(data.port == window.location.port) {
            appendText(data.text)
        }
    })
    
    furhat.send({
        event_name: 'furhatos.event.requests.RequestSkillGUIName',
        port: window.location.port,
    })
})

function setPageTitle(title) {
    document.getElementsByTagName("title")[0].innerText = title
}

function appendText(text) {
    var p = document.createElement('p')
    
    p.innerText = text
    document.getElementById('root').appendChild(p)
}

function clearScreen() {
    var root = document.getElementById('root')

    while (root.firstChild) {
        root.removeChild(root.firstChild)
    }
}