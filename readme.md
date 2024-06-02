# Smart City Ulm: Air Quality Analysis 
---

### Project Status

**Note:** This project is currently undergoing refactoring and improvement. I am in the process of enhancing the codebase to improve maintainability, performance, and extendibility. Please expect changes and updates as we work to make these improvements. Your understanding and patience are appreciated.

---
## Executive Summary:

Leveraging advanced air quality monitoring at Eselsberg, this project focuses on the critical insights provided by the Lupferbrücke sensor. Despite a reduction in the number of active sensors, the data from this single sensor is instrumental in addressing key urban issues. This includes issuing timely health advisories, optimizing traffic management, and fostering public awareness about environmental conditions. By analyzing this data, Ulm can develop strategic plans for urban development, enhance public health measures, and engage the community in pollution reduction efforts. The continued operation of this sensor highlights Ulm's dedication to sustainability and public well-being.

### Business Problem:

The city of Ulm’s investment in advanced air quality monitoring at Eselsberg, despite scaling down to the single Lupferbrücke sensor, remains pivotal. This sensor's data enables the city to tackle key issues: issuing health advisories during high pollution periods to protect vulnerable groups, optimizing traffic management to reduce vehicular emissions, and fostering environmental awareness. By analyzing this critical data, Ulm can develop informed strategies for urban planning, enhance public health initiatives, and drive community engagement in pollution reduction. The continued operation of this sensor underscores the city's commitment to sustainability and public well-being.

### Methodology:

1. Extracted data via API using Python; scraped additional weather data using Selenium for web automation.
2. Conducted an exploratory data analysis (EDA) on the full dataset with all sensors to understand data, thresholds, and overall air quality in Ulm.
3. Conducted an EDA to find data patterns for forecasting, utilizing machine learning techniques.
4. Trained multiple machine learning models to predict air quality levels.
