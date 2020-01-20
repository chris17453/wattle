


# Database

# login
- generates a session
- populates  id = user id
- entity=dict of entity info


# menu
- The menu is generated from the LINKS table
    - The menu loads all groups assigned 
    - to you, and then all links assigned to those groups. 
    - the menu groups are sorted by ordinal
    - the links in the groups are sorted by ordinal
- Groups =Menu Dropdowns
- Links represent a single method.
- A method may have many links.
- Links have Display customizations
- the URL format is the unique format "m/{entity}/{method}"
- the menu is regenerated every page load, and placed into the session

