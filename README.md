<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>
<!-- PROJECT HEADER -->
<h3 align="center">StarOS Health Check</h3>

  <p align="center">
    Health Check for StarOS using Pyats and Genie frameworks
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This health Check is intended to be an automation tool for all Cisco StarOS devices during the execution of MW or Babysittings and avoid repetitive task or human flaws.


<!-- GETTING STARTED -->
## Getting Started

Copy project

```
git clone https://github.com/apatino18/HC_ATT_Cisco.git
```

### Prerequisites

You must have installed Docker on your computer

- Get Docker from : https://docs.docker.com/get-docker/

- Guide for Docker: https://docs.docker.com/get-started/

- Basic Docker Tutorial (Spanish) : https://www.youtube.com/watch?v=4Dko5W96WHg&t=7s


### Installation

1. Edit your *username* and *password* inside of file *node_table* file inside **_HC_FILES_** directory

![Screenshot 2022-08-18 120432](https://user-images.githubusercontent.com/101678467/185453566-3617c3b3-f2a7-4f25-a166-d5d18b2ec08b.png)

![Screenshot 2022-08-24 172003](https://user-images.githubusercontent.com/101678467/186534340-e8d4f518-131e-4001-86e3-4b49742c91ff.png)
 </br>
 </br>
2. Modify Parameters to evaluate during Health Check (OPTIONAL)

![Screenshot 2022-08-24 172548](https://user-images.githubusercontent.com/101678467/186534341-88369667-7eeb-40f0-bd99-b48a76a1ad3c.png)

3. Create Docker Image Based on *dockerfile*
```
docker build -t health_check .
```

4. Start Docker Container Based on result image named *health_check* Modify (directory_path) with your own path

```
docker run -dt --name HC_staros -p 8080:8080 -v <directory_path>:/HC_reports/ health_check
```

<sub>
<br>
NOTE: WINDOWS ONLY
</br>
When you replace the directory path on windows you should see something like this:
<br>
C:\Users\apatinoz\Deskto\TEST\HC_STORAGE\  
</br>
<br>
You will need to replace the "\" with "/"
</br>
C:/Users/apatinoz/Desktop/TEST/HC_STORAGE/ 
</sub>
<br>
</br>
5.  Generate your TESTBED (nodes to execute your Health Check)
<br>
</br>
Modify (customer_testbed.yml) with your customer Name
<br>
</br>
Example:
ATT_testbed.yml

```
docker exec -it HC_staros bash  -c "cd /healthcheck/; pyats create testbed file --path /healthcheck/node_table.xlsx --output /healthcheck/customer_testbed.yml --encode-password"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

- To execute a Health Check:
Modify *Customer_testbed.yml* with your OWN testbed created on STEP 5).

Custom parameters:
- customer_param (Parameters to failed or pass the Health Check execution)
- nodes (Tesbed generates on step 5, you can have more than 1 testbed)
- hc_type (execution type, at this moment only existe one health check but we planned more features on the roadmap)
- html-logs (Generate html report to share with your customer or team)

```
docker exec -it HC_staros bash  -c "cd /healthcheck/ ; pyats run job HC_ASR.py --customer_param HC_param.yml --nodes customer_testbed.yml --hc_type staros_basic_healthcheck.py --html-logs"
```

- Review all Health Checks executed:
```
docker exec -it HC_staros bash -c "pyats logs view --host 0.0.0.0 --port 8080"
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] New Babysitting Script
- [ ] Add new Commands to parse StarOS
- [ ] SSD and config compare afte MW
- [ ] Save config and modify priorities

See the [open issues](https://github.com/apatino18/HC_ATT_Cisco/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Arturo Patino - apatinoz@cisco.com

Project Link: [https://github.com/apatino18/HC_ATT_Cisco](https://github.com/apatino18/HC_ATT_Cisco)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
