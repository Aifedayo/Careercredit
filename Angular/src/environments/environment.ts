// This file can be replaced during build by using the `fileReplacements` array.
// `ng build ---prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
 // API_URL:`http://34.215.123.78:4000/`,
 //  API_URL:`http://stage.linuxjobber.com:4000/`,
  // WS_URL:`ws://stage.linuxjobber.com:4000`,
  // WS_URL:`wss://e1s0jb46bg.execute-api.us-east-2.amazonaws.com/test`,
    WS_URL:`wss://85zctiv75k.execute-api.us-east-2.amazonaws.com/test`,
  // API_URL:`http://34.213.31.144:4000/`,
  API_URL:`http://localhost:8000/`,

  production: false
};

/*
 * In development mode, for easier debugging, you can ignore zone related error
 * stack frames such as `zone.run`/`zoneDelegate.invokeTask` by importing the
 * below file. Don't forget to comment it out in production mode
 * because it will have a performance impact when errors are thrown
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
