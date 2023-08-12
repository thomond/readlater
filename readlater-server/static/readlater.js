var lastModifiedTS = 0
var FQDN = "http://192.168.0.2:5000"


// Queries last modified to ascertain if DB has been updated recently
async function chkIfNewData() {
	const modified = await fetch(`${FQDN}/last_modified`)
		.then(response => response.json())
		.then(data => {
			return data.last_modified
		})
		.catch(error => console.error(error))
	// Update last modified value if needs be and return if there is neew data to fetch
	if (modified == lastModifiedTS)
		return false
	else
		lastModifiedTS = modified
		return true
}

// Fetch data then parse json then for each object in array 
function fetchUrls() {
	fetch(`${FQDN}/urls`)
		.then(response => response.json())
		.then(data => {
			// Clear area
			document.getElementById('unread-container').innerHTML = ''
			unreadItems = data.filter(url => !url.read_status)
			unreadItems.forEach(url => {
				liElement = processUrl(url)
				document.getElementById('unread-container').appendChild(liElement)
			})

			document.getElementById('read-container').innerHTML = ''
			readItems = data.filter(url => url.read_status)
			readItems.forEach(url => {
				liElement = processUrl(url)
				document.getElementById('read-container').appendChild(liElement)
			})
		})
		.catch(error => console.error(error))
}


// Function to create the list
function processUrl(url){
	const liElement = document.createElement('li')
	const urlElement = document.createElement('a')
	const inputElement = document.createElement('button')
	urlElement.href = url.url
	urlElement.textContent = url.url
	urlElement.target= "_blank"
	// if item is read add strikethough effect and option to unmark
	if(url.read_status){
		inputElement.textContent = "(Unmark as read)"
		inputElement.onclick  = () => { markAsRead(url.id) }
		
		liElement.className = "strikeout"
		// Append elements to li and then the container
		liElement.appendChild(urlElement)
		liElement.appendChild(inputElement)
	}else{// Otherwise the URL can be clicked on to be marked as read
		// Set onClick event to mark only if it's unread
		urlElement.onclick = (event) => { 
			markAsRead(url.id) 
		}
		liElement.appendChild(urlElement)


	}

	return liElement
	
}

async function markAsRead(id){
	const url = `${FQDN}/mark/${id}`
	const options = {
		method: 'POST'
	}
	
	fetch(url,options)
		.then(response => response.json())
		.then(data => {
			if(data.success){
				console.info(`${id} marked as read`)
				// Force refresh
				fetchUrls()
			}else{
				console.error(data.error)
			}
		} )
		.catch(error => console.error(error))
	
	
}

// Fetch the URLs once and then  every 5 seconds when update is needed
fetchUrls()
setInterval(() => {
	chkIfNewData().then( (needsUpdate) => {
		if(needsUpdate)
			fetchUrls()
	})
	
}, 10000)