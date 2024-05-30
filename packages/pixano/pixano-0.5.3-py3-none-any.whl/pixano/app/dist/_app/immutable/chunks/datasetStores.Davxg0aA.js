import{t as M,a as v}from"./index.D__UofN6.js";import{M as I}from"./scheduler.Cq5UBZ1T.js";import{w as _}from"./entry.BGJCdFkn.js";function z(e){return(e==null?void 0:e.length)!==void 0?e:Array.from(e)}function j(e,f){M(e,1,1,()=>{f.delete(e.key)})}function C(e,f){e.f(),j(e,f)}function G(e,f,h,m,w,d,s,u,n,L,S,k){let c=e.length,l=d.length,i=c;const y={};for(;i--;)y[e[i].key]=i;const g=[],A=new Map,T=new Map,E=[];for(i=l;i--;){const t=k(w,d,i),o=h(t);let a=s.get(o);a?m&&E.push(()=>a.p(t,f)):(a=L(o,t),a.c()),A.set(o,g[i]=a),o in y&&T.set(o,Math.abs(i-y[o]))}const D=new Set,b=new Set;function p(t){v(t,1),t.m(u,S),s.set(t.key,t),S=t.first,l--}for(;c&&l;){const t=g[l-1],o=e[c-1],a=t.key,r=o.key;t===o?(S=t.first,c--,l--):A.has(r)?!s.has(a)||D.has(a)?p(t):b.has(r)?c--:T.get(a)>T.get(r)?(b.add(a),p(t)):(D.add(r),c--):(n(o,s),c--)}for(;c--;){const t=e[c];A.has(t.key)||n(t,s)}for(;l;)p(g[l-1]);return I(E),g}function N(e,f){const h={},m={},w={$$scope:1};let d=e.length;for(;d--;){const s=e[d],u=f[d];if(u){for(const n in s)n in u||(m[n]=1);for(const n in u)w[n]||(h[n]=u[n],w[n]=1);e[d]=u}else for(const n in s)w[n]=1}for(const s in m)s in h||(h[s]=void 0);return h}function V(e){return typeof e=="object"&&e!==null?e:{}}const x=20,B=1;/**
 * @copyright CEA
 * @author CEA
 * @license CECILL
 *
 * This software is a collaborative computer program whose purpose is to
 * generate and explore labeled data for computer vision applications.
 * This software is governed by the CeCILL-C license under French law and
 * abiding by the rules of distribution of free software. You can use,
 * modify and/ or redistribute the software under the terms of the CeCILL-C
 * license as circulated by CEA, CNRS and INRIA at the following URL
 *
 * http://www.cecill.info
 */const F={currentPage:B,pageSize:x},Z=_(),q=_([]),H=_(!1),J=_(F),K=_({shouldSave:!1,canSave:!1});export{B as D,V as a,J as b,F as c,Z as d,z as e,C as f,N as g,x as h,H as i,q as m,j as o,K as s,G as u};
