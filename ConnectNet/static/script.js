// Sample data


/*const peopleData = [
    { name: "Alice Johnson", following: false },
    { name: "Bob Smith", following: true },
    { name: "Charlie Brown", following: false },
    { name: "Diana Prince", following: true }
];

const friendsData = peopleData.filter(person => person.following); */


function resetTabs(){
    const tabs = document.querySelectorAll('.tab');
    const content = document.getElementById('content');
    tabs.forEach(tab => tab.classList.remove('active'));
   
}

function appendData(contentHtml){
    
    const content = document.getElementById('content');
    content.innerHTML = contentHtml;
}

/*function getFeeds(){

    let contentHtml = '';
    const feedData = [
        { title: "New Feature Release", message: "We've just launched our new messaging system!", time: new Date('2024-10-13T10:30:00') },
        { title: "Community Update", message: "Join us for our monthly virtual meetup this Friday!", time: new Date('2024-10-12T15:45:00') },
        { title: "Tech Tip of the Day", message: "Learn how to optimize your workflow with these 5 simple tricks.", time: new Date('2024-10-11T09:00:00') }
    ];

    contentHtml = `
                <h2>Feed</h2>
                ${feedData.sort((a, b) => b.time - a.time).map(item => `
                    <div class="message">
                        <h3>${item.title}</h3>
                        <p>${item.message}</p>
                        <span class="time">${item.time.toLocaleString()}</span>
                    </div>
                `).join('')}
            `;
    
    appendData(contentHtml);
}*/

let blogdata;
async function getFeeds(){

     // Function to make the GET request
     try {
        const response = await fetch('/blog');
        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the JSON response
        blogdata = await response.json();
        console.log(blogdata); // Handle the data as needed
        let contentHtml = '';
        contentHtml = `
                <h2>Feed</h2>
                ${blogdata.sort((a, b) => b.time - a.time).map(item => `
                    <div class="message">
                        <h3>${item.subject}</h3>
                        <p>${item.description}</p>
                        <span class="time">${item.time.toLocaleString()}</span>
                    </div>
                `).join('')}
            `;
    
    appendData(contentHtml);


    }catch (error) {
        console.error('Error fetching data:', error);
    }
}

function loadFeed(){
    resetTabs();
    document.getElementById('default').classList.add('active');
    getFeeds();
}

let peopledata;
async function getPeople(){

    
    // Function to make the GET request
    try {
        const response = await fetch('/users');
        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the JSON response
        peopledata = await response.json();
        console.log(peopledata); // Handle the data as needed
        let contentHtml = '';
        contentHtml = `
                <h2>People</h2>
                ${peopledata.map(person => `
                    <div class="person">
                        <h3>${person.name}</h3>
                        <button onclick="toggleFollow(this, ${person.id})" class="${person.following ? 'following' : ''}">
                            ${person.following ? 'Following' : 'Follow'}
                        </button>
                    </div>
                `).join('')}
            `;
        appendData(contentHtml);


    }catch (error) {
        console.error('Error fetching data:', error);
    }


    

    /*function toggleFollow(button, name) {
        
        const person = peopleData.find(p => p.name === name);
        if (person) {
            person.following = !person.following;
            button.textContent = person.following ? 'Following' : 'Follow';
            button.classList.toggle('following');
            
            // Update friendsData
            if (person.following) {
                if (!friendsData.includes(person)) {
                    friendsData.push(person);
                }
            } else {
                const index = friendsData.findIndex(f => f.name === name);
                if (index > -1) {
                    friendsData.splice(index, 1);
                }
            }
        }
    }*/
    
    /*let contentHtml = '';
    const peopleData = [
        { name: "Alice Johnson", following: false },
        { name: "Bob Smith", following: true },
        { name: "Charlie Brown", following: false },
        { name: "Diana Prince", following: true }
    ];

    contentHtml = `
                <h2>People</h2>
                ${peopleData.map(person => `
                    <div class="person">
                        <h3>${person.name}</h3>
                        <button onclick="toggleFollow(this, '${person.name}')" class="${person.following ? 'following' : ''}">
                            ${person.following ? 'Following' : 'Follow'}
                        </button>
                    </div>
                `).join('')}
            `;
    
    appendData(contentHtml);*/
}

function toggleFollow(button, id) {
        
    const person = peopledata.find(p => p.id === id);
    if (person) {
        
        person.following = !person.following;
        button.textContent = person.following ? 'Following' : 'Follow';
        button.classList.toggle('following');
        // Update friendsData
        if (person.following) {
            fetch ('/follow/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({})})
        } else {
            fetch ('/unfollow/'+id,{method:'DELETE',headers:{'Content-Type':'application/json'},body:JSON.stringify({})})
        }
        
    }
}


function loadPeople(){
    resetTabs();
    document.getElementById('people').classList.add('active');
    getPeople();
}

async function getInsights(){
    let contentHtml = '';

    const response = await fetch('/insights');
    
    insightsdata = await response.json();
    console.log(insightsdata); // Handle the data as needed
    
    const insightsarray = Object.values(insightsdata)
    console.log(insightsarray);
    contentHtml = `
                <h2>Messgae Insights</h2>
                ${insightsarray.map(item => `
                    <div class="message">
                        <h3>${item}</h3>
                        <!-- <button id={item.id} onclick="getDescription({item.id})">Get Description</button> -->
                    </div>
                `).join('')}
            `;
    appendData(contentHtml);
}


function loadInsights(){
    resetTabs();
    document.getElementById('insights').classList.add('active');
    getInsights();
}

function getDescription(id){
    alert(id);
}



/** 

function changeTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    const content = document.getElementById('content');

    tabs.forEach(tab => tab.classList.remove('active'));
   
    event.target.classList.add('active');

    let contentHtml = '';
    switch (tabName) {
        case 'feed':
            contentHtml = `
                <h2>Feed</h2>
                ${feedData.sort((a, b) => b.time - a.time).map(item => `
                    <div class="message">
                        <h3>${item.title}</h3>
                        <p>${item.message}</p>
                        <span class="time">${item.time.toLocaleString()}</span>
                    </div>
                `).join('')}
            `;
            break;
        case 'friends':
            contentHtml = `
                <h2>Friends</h2>
                ${friendsData.map(friend => `
                    <div class="friend">
                        <h3>${friend.name}</h3>
                        <p>Following</p>
                    </div>
                `).join('')}
            `;
            break;
        case 'people':
            contentHtml = `
                <h2>People</h2>
                ${peopleData.map(person => `
                    <div class="person">
                        <h3>${person.name}</h3>
                        <button onclick="toggleFollow(this, '${person.name}')" class="${person.following ? 'following' : ''}">
                            ${person.following ? 'Following' : 'Follow'}
                        </button>
                    </div>
                `).join('')}
            `;
            break;
    }
    content.innerHTML = contentHtml;
} */

async function addPost(){
    subject = document.getElementById('post-title').value;
    desc = document.getElementById('post-message').value;
    console.log(subject)
    console.log(desc)
    const data = {
        subject:subject,
        desc:desc
    };
    const response = await fetch ('/blog',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})

        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the JSON response
        blogdata = await response.json();
        console.log(blogdata); // Handle the data as needed
        window.location.href = "/home"
    
}


// Initialize the page with the Feed tab active
window.addEventListener('load',function(){
    loadFeed();
});


