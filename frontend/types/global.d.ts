import React from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      [elementName: string]: any;
    }
  }
  
  interface ProcessEnv {
    NEXT_PUBLIC_API_URL: string;
  }
  
  namespace NodeJS {
    interface ProcessEnv {
      NEXT_PUBLIC_API_URL: string;
    }
  }
} 