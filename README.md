# Shockfish
 
`Shockfish` is a classic  experimental Python-based web application firewall (WAF).

Its main goals are to demonstrate common application security methods and algorithms implemented in WAFs,
help web developers and security engineers better understand the processes of web applications firewalling , and illustrate some fundomental problems of this technology.

## Installation

```
git clone https://github.com/PositiveTechnologies/shockfish.git
cd shockfish
python3 setup.py install
```

## Deployment

`Shockfish` config file is located at `/etc/shockfish/shockfish.json` by default.

The following config lets you protect a `www.example.com` web-application, which has `192.168.2.2` IP-address.

1. Specify a protected web-server:
 ```
{
    "backend": {
        "host": "192.168.2.2",
        "port": 80
    },
    ...
}
 ```

2. Specify a virtual server interface and port:

 ```
{
    "virtual": {
        "interface": "192.168.1.2",
        "port": 80
    },
    ...
}
 ``` 

3. Add the following record to `/etc/hosts` or configure DNS server:

 ```
192.168.1.2 www.example.com
 ```

4. Run the following command:

 ```
sudo python3 -m shockfish
 ```

## Description

### Core

`Shockfish` core is based on the `Twisted` framework. 

Restrictions:
1. It supports only a `reverse proxy` mode.
2. It does not support URL rewriting, so you should run `shockfish` on the same port as a protected web-application.


### Protectors

`Shockfish` implements classic protection mechanisms (protectors) against the following attacks:
* Reflected Cross-Site Scripting (XSS)
* DOM-based XSS
* CRLF injection
* SQL injection
* SSRF
* LDAP injection

Protection against DOM-based XSS is performed on a client-side using [shockfish.js](https://github.com/PositiveTechnologies/shockfish.js.git) JavaScript module. All detected DOM-based XSS are blocked and logged into the browser console.

### Attacks

`Shockfish` has some weaknesses and vulnerabilities in normalization, parsing and protectors. That is why it is vulnerable to the following classic attacks:
* HPP
* HPC
* parsing differentials


## References

### English
1. [Waf.js: How to Protect Web Applications using JavaScript.](http://www.slideshare.net/DenisKolegov/wafjs-how-to-protect-web-applications-using-javascript)
2. [Waf.js: How to Protect Web Applications using JavaScript (video).](https://www.youtube.com/watch?v=YAyKzLEU-JE)

### Russian
1. [Who said WAF? (video)](https://www.youtube.com/watch?v=KJrhdYvZTBE)
2. [Who said WAF?](https://www.slideshare.net/pdug_slides/waf-70362519)
3. [Web Application Security Methods and Algorithms.](https://www.slideshare.net/dnkolegov/ss-65852359)
4. [Waf.js: How to Protect Web Applications using JavaScript (video)](https://www.youtube.com/watch?v=j207ThTQjFc)
5. [Waf.js: How to Protect Web Applications using JavaScript.](https://www.slideshare.net/phdays/wafjs-javascript)
