# Paya [radio in tray]

It's simple radio player in tray. You can set like or dislike, change station, skip tracks and wiev info about current track.
Paya also have web panel, where present similiar functions.

Web panel will be available on ip your pc, but by default it can be opened only from your pc.  
- If you need to open web panel from other devicec in your local network, to set ```is_accept_outside_query``` to true in config.yaml  
- If you want open web panel with paya automaticly to set ```is_open_browser_at_startup``` to true in config.yaml

Paya can run over proxy connections. For this is to set ```proxy -> enabled``` to true in config.yaml
and fill connection fields (address, port) if need proxy auth, fill user and password fields

# How to run

```bash
./install.sh
```

Next, you can find application desktop entry in main menu


# Frontend part for remote web control

## For develop

- The first is to set ```is_develop``` to true in config.yaml. This option specifies that the project does not use an already built frontent. Instead, the development server on port 7777 will be used.

- Second - run dev server

``` bash
# open subproject dir
cd frontend

# install dependencies
npm install

# serve with hot reload at localhost:7777
npm run dev
```

## For apply changes

```bash
# build for production with minification
npm run build

```
