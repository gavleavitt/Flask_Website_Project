const clientId = 'EaXzJp8eDUGAKE3U';
const redirectUri = 'http://localhost:5000/webapps/lacoswtrace/laco-sw-trace-app-protected';

require(["esri/portal/Portal","esri/identity/OAuthInfo","esri/identity/IdentityManager","esri/portal/PortalQueryParams","esri/layers/FeatureLayer"],
  function (Portal, OAuthInfo, esriId, PortalQueryParams, FeatureLayer) {
    // const personalPanelElement = document.getElementById("personalizedPanel");
    // const anonPanelElement = document.getElementById("anonymousPanel");
    // const userIdElement = document.getElementById("userId");
    const info = new OAuthInfo({
      appId: clientId,
      popup: false
    });

    esriId.registerOAuthInfos([info]);
    esriId
      .checkSignInStatus(info.portalUrl + "/sharing")
      .then(() => {
        const portal = new Portal();
        // Setting authMode to immediate signs the user in once loaded
        portal.authMode = "immediate";
        //
        portal.load().then(() => {
          const gravitymainsFeatures = new FeatureLayer({
            title: "Gravity Mains",
            url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/GravityMains_Simplify_2ft/FeatureServer/0",
            listMode: "hide",
            // minScale: 25000,
            minScale: 15000,
            popupTemplate: popupGM,
            renderer: gravityMainsCIM,
            // labelingInfo: [gravityMainsLabels]
            const lateralFeatures = new FeatureLayer({
              title: "Laterals",
              url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Laterals/FeatureServer/0",
              minScale: 25000,
              popupTemplate: popupLat
            });

            const inletFeatures = new FeatureLayer({
              title: "Inlets",
              // url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/inlets_wgs84/FeatureServer/0",
              url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Inlets_SHP/FeatureServer/0",
              minScale: 15000,
              popupTemplate: popupIN
            });
            const mhFeatures = new FeatureLayer({
              title: "Maintenance Holes",
              url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/maintenanceholes/FeatureServer/0",
              minScale: 15000,
              popupTemplate: popupMH
            });

             const olFeatures = new FeatureLayer({
              title: "Outlets",
               url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/outlets/FeatureServer/0",
               minScale: 15000
             });
             gravityMainsGrouped = new GroupLayer({
               id: "gmgroup",
               title: "Gravity Mains",
               layers: [gravitymainsFeatures,gravityMainsVTL],
               visibilityMode: "inherited"
             })
             const networklayer = new GroupLayer({
                 id: "networklayer",
                 title: "Storm Network",
                 layers: [lateralFeatures, gravityMainsGrouped, inletFeatures, mhFeatures, olFeatures]
                 // layers: [lateralFeatures, gravitymainsFeatures, inletFeatures, mhFeatures, olFeatures]
               });
          });
        })
      })
      .catch(() => {
        // Not logged in, prompt user to log in
        console.log(info.portalUrl)
        esriId.getCredential(info.portalUrl + "/sharing")
        // window.open(esriId.getCredential(info.portalUrl + "/sharing"))
        // anonPanelElement.style.display = "block";
        // personalPanelElement.style.display = "none";
      });

    // document.getElementById("sign-in").addEventListener("click", () => {
    //   // user will be redirected to OAuth Sign In page
    //   esriId.getCredential(info.portalUrl + "/sharing");
    // });
    //
    // document.getElementById("sign-out").addEventListener("click", () => {
    //   esriId.destroyCredentials();
    //   window.location.reload();
    // });

    // function displayItems() {
    //   const portal = new Portal();
    //   // Setting authMode to immediate signs the user in once loaded
    //   portal.authMode = "immediate";
    //   // Once loaded, user is signed in
    //   portal.load().then(() => {
    //     // Create query parameters for the portal search
    //     const queryParams = new PortalQueryParams({
    //       query: "owner:" + portal.user.username,
    //       sortField: "numViews",
    //       sortOrder: "desc",
    //       num: 20
    //     });
    //   };
    // };
});
// const signInButton = document.getElementById('sign-in');
// do this on a button click to avoid popup blockers
// document.addEventListener('click', function(){
//     window.open('https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id='+clientId+'&response_type=token&expiration=20160&redirect_uri=' + window.encodeURIComponent(redirectUri), 'oauth-window', 'height=400,width=600,menubar=no,location=yes,resizable=yes,scrollbars=yes,status=yes')
// });
// window.open('https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id='+clientId+'&response_type=token&expiration=20160&redirect_uri=' + window.encodeURIComponent(redirectUri), 'oauth-window', 'height=400,width=600,menubar=no,location=yes,resizable=yes,scrollbars=yes,status=yes')

// const info = new OAuthInfo({
//   // Swap this ID out with registered application ID
//   appId: "qrmZmPws0mBP02gI",
//   popup: false
// });
// // Register OAuthinfo with IdentityManager
// esriId.registerOAuthInfos([info]);
// // Check if user is signed in
// esriId
//   .checkSignInStatus(info.portalUrl + "/sharing")
//   .then(() => {
//     displayItems();
//   })
//   .catch(/*give user an option to sign in*/);
//
