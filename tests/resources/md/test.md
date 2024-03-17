# Spring
- ![spring overview graph](java-spring-overview.png)
- [start.string.io](https://start.spring.io/)

---
<!--ID:1708351328890-->
1. Lifecycle of SpringBoot application:
> ### 1. Application Launch
> - **Starting Point**: begins with `main` method, which typically calls `SpringApplication.run(App.class, args)`, where `App.class` is class annotated with `@SpringBootApplication`.
> - **Initial Setup**: `SpringApplication` prepares the environment, sets up logging, and starts the process of creating the Spring application context.
>
> ### 2. Environment Preparation
> - **Configuration Properties**: loads configuration properties from various sources (properties files, environment variables, command-line arguments) to configure the application context.
>
> ### 3. Creation of ApplicationContext
> - **ApplicationContext Type Determination**: decides `StandardServletWebServerApplicationContext` or `AnnotationConfigApplicationContext` for non-web applications.
> - **BeanFactory Preparation**: application context initializes `BeanFactory`, which is responsible for creating and managing Spring beans.
>
> ### 4. @Configuration Beans Processing
> - **Component Scanning**: Spring Boot scans for components (`@Component`, `@Service`, `@Repository`, `@Controller`) and configuration (`@Configuration`) classes. This scanning is triggered by `@SpringBootApplication`, which implicitly includes `@ComponentScan` and `@EnableAutoConfiguration`.
> - **Configuration Class Processing**: `@Configuration` classes are processed to register bean definitions. For each `@Bean` method in `@Configuration` classes, a bean definition is created and registered in the `BeanFactory`.
>     - **Dependency Resolution**: Beans are created in a topological order based on their dependencies. If a bean depends on another, the dependencies are instantiated first.
>     - **Proxy Creation**: For `@Configuration` classes, CGLIB proxies are created to ensure that `@Bean` methods within the same configuration class are intercepted to reuse the same instance, adhering to the singleton pattern.
>
> ### 5. Auto-Configuration
> - **@EnableAutoConfiguration**: Part of `@SpringBootApplication`, triggers Spring Boot's auto-configuration mechanisms, which configure beans based on the classpath and defined properties.
> - **Conditional Configuration**: Spring Boot evaluates conditions (`@ConditionalOnClass`, `@ConditionalOnBean`, etc.) to decide which auto-configuration classes should be applied.
>
> ### 6. Application Context Refresh
> - **Bean Instantiation**: All bean definitions registered in the `BeanFactory` are instantiated, including executing `@Bean` methods in `@Configuration` classes.
> - **Lifecycle Processing**: Beans implementing `InitializingBean`, annotated with `@PostConstruct`, or defined with custom `init-methods` are initialized accordingly.
> - **Event Publishing**: `ApplicationContext` publishes lifecycle events (`ContextRefreshedEvent`, `ApplicationReadyEvent`, etc.) that can be consumed by beans within the context.
>
> ### 7. Web Server Initialization (If applicable)
> - **Embedded Server Start**: For web applications, Spring Boot starts the embedded web server (Tomcat, Jetty, or Undertow) and registers the application context as a Servlet context.
>
> ### 8. Application Ready
> - **Ready to Serve**: The application is fully initialized, and Spring Boot logs the "Started Application in X seconds" message.
>
> ### Optimization Tips
> - **Lazy Initialization**: defer creation of beans until they are needed. This can be done by setting `spring.main.lazy-initialization=true` in `application.properties`.
> - **Conditional Beans**: Use conditional annotations (`@ConditionalOnProperty`, `@ConditionalOnMissingBean`, etc.) to prevent unnecessary beans from being created.
> - **Profile-Specific Configuration**: Utilize Spring Profiles to only load certain beans or configurations under specific runtime conditions.
>
> ### Shutdown
> 1. **Trigger Shutdown**: The shutdown process can be initiated in various ways, such as a SIGTERM signal, a call to `SpringApplication.exit()`, or programmatically closing the `ApplicationContext`.
> 2. **Context Closed Event**: Spring raises a `ContextClosedEvent`. This event is published in the application context to signal that the context is about to be closed. Beans that implement the `DisposableBean` interface or use the `@PreDestroy` annotation can listen for this event to perform cleanup operations.
> 3. **Pre-Destroy Methods**: Spring calls `@PreDestroy` annotated methods and `DisposableBean.destroy()` methods on beans. These methods are intended for releasing resources that the bean might be holding (like closing database connections, stopping threads, or releasing file handles).
> 4. **Stop Web Server (if applicable)**:
> 6. **Application Exit**: If the shutdown was initiated by calling `SpringApplication.exit()`, the application could return an exit code. In case of a JVM shutdown (e.g., SIGTERM), the JVM process terminates.
> 7. **JVM Shutdown Hooks**: automatically registers a shutdown hook with the JVM to ensure that `ApplicationContext` is closed gracefully on JVM shutdown. Custom shutdown hooks can also be registered by the application for performing cleanup tasks right before the JVM exits.

<!--ID:1706289784918-->
1. Common Spring annotations:
> **`@SpringBootApplication`**: Indicates a configuration class that declares one or more `@Bean` methods and also triggers auto-configuration and component scanning.
> Convenience annotation for `@Configuration`, `@EnableAutoConfiguration`, and `@ComponentScan`
> - @Configuration: Tags class as a source of bean definitions for the application context.
> - @EnableAutoConfiguration: Tells Spring Boot to start adding beans based on classpath settings, other beans, and various property settings.
> - @ComponentScan: Tells Spring to look for other components, configurations, and services in the current package
> ```java
> @SpringBootApplication
> public class MyApp {
>     public static void main(String[] args) {
>         SpringApplication.run(MyApp.class, args);
>     }
> }
> ```
>
> **`@Autowired`**: Marks a constructor, field, setter method, or config method as to be autowired by Spring's dependency injection facilities.
> ```java
> @Service
> public class MyService {
>     @Autowired
>     private MyRepository repository;
> }
> ```
>
> **`@Bean`**: Indicates that a method produces a bean to be managed by the Spring container.
> ```java
> @Configuration
> public class AppConfig {
>     @Bean
>     public MyBean myBean() {
>         return new MyBean();
>     }
> }
> ```
>
> **`@Component`**: Indicates that a class is a Spring component. It’s a generic stereotype for any Spring-managed component.
> ```java
> @Component
> public class MyComponent {}
> ```
>
> **`@Service`**: Indicates that a class is a service. It’s used to annotate classes that perform service tasks, often from business logic.
> - for service layer classes, follows Spring three-layer architecture: controllers, services, and repositories
> - you can use `@Component` instead of `@Service` without impacting Spring's behavior
> ```java
> @Service
> public class MyService {}
> ```
>
> **`@Repository`**: Indicates that a class is a repository, which is a mechanism for encapsulating storage, retrieval, and search behavior from a data store.
>  ```java
>  @Repository
>  public interface MyRepository extends JpaRepository<MyEntity, Long> {}
>  ```
>
> **`@Transactional`**: Indicates that a method or class should have transactional semantics; for example, a method may need to be executed within a transactional context.
> ```java
> @Service
> public class MyService {
>     @Transactional
>     public void updateData() {
>         // transactional code here
>     }
> }
> ```
>
> **`@Configuration`**: Indicates that a class is a source of bean definitions.
> ```java
> @Configuration
> public class AppConfig {
>     @Bean
>     public MyBean myBean() {
>         return new MyBean();
>     }
> }
> ```
>
> **`@Value`**: Used to inject property values into components, typically from a properties file.
> ```java
> @Component
> public class MyComponent {
>     @Value("${my.property}")
>     private String myProperty;
> }
> ```
>
> **`@Profile`**: Indicates that a component is eligible for registration when one or more specified profiles are active.
> ```java
> @Service
> @Profile("dev")
> public class DevOnlyService {}
> ```
>
> **`@Scheduled`**: Used for declaring methods as scheduled tasks, which will be executed at a fixed interval or cron expression.
> ```java
> @Component
> public class ScheduledTasks {
>     @Scheduled(fixedRate = 1000)
>     public void reportCurrentTime() {
>         // task code here
>     }
> }
> ```
>
> **`@Qualifier`**: Used along with `@Autowired` to specify which bean should be injected when there are multiple candidates.
> ```java
> @Service
> public class MyService {
>     @Autowired
>     @Qualifier("specificBean")
>     private MyBean myBean;
> }
> ```

<!--ID:1706512032841-->
1. Explain `@Transactional`:
> 1. **Transaction Management**: ensures that DB related method is executed within related transactional context. If no transaction is in progress, it starts a new one. If there's an existing transaction, the method can join that transaction, depending on the propagation settings.
>
> 2. **Propagation Behavior**: Common behaviors include `REQUIRED` (join an existing transaction or start a new one if none exists), `REQUIRES_NEW` (always start a new transaction), and others. This dictates how transactions are managed across multiple method calls.
>
> 3. **Isolation Levels**: You can specify the isolation level of the transaction, which determines how visible the changes made by this transaction are to other transactions running concurrently. This helps in managing concurrent access to the database and prevents issues like dirty reads, non-repeatable reads, and phantom reads.
>
> 4. **Rollback Behavior**: By default, a transaction will be rolled back if a runtime exception (unchecked exception) is thrown within the method. You can customize this behavior using the `rollbackFor` and `noRollbackFor` attributes
>
> 5. **Read-Only Optimization**: You can mark a transaction as read-only, which can be a performance optimization. Some databases can optimize transactions that are read-only.
>
> 6. **Transaction Synchronization**: registering resources like JDBC connections or Hibernate sessions with the transaction.
>
> 8. **Aspect-Oriented Programming (AOP)**: implemented using AOP proxies
>
> 9. **Database and JPA/Hibernate Integration**: often used with JdbcTemplate, JPA, or Hibernate integration, ensures that database operations performed within the transactional method are part of the same database transaction.
>
> 10. **Integration with Other Frameworks**: can be used with other resources that support transactions, like JMS or JTA, allowing for distributed transactions across multiple systems.
> ```java
> @Entity
> public class User {
>     @Id
>     @GeneratedValue(strategy = GenerationType.AUTO)
>     private Long id;
>     private String name;
>     private String email;
>     // Constructors, getters, setters...
> }
>
> public interface UserRepository extends JpaRepository<User, Long> {
>     // Custom query methods if needed
> }
>
> @Service
> public class UserService {
>
>     private final UserRepository userRepository;
>
>     public UserService(UserRepository userRepository) {
>         this.userRepository = userRepository;
>     }
>
>     @Transactional
>     public void createUser(String name, String email) {
>         User user = new User();
>         user.setName(name);
>         user.setEmail(email);
>         userRepository.save(user);
>     }
>
>     @Transactional(readOnly = true)
>     public User getUser(Long id) {
>         return userRepository.findById(id).orElseThrow(() -> new RuntimeException("User not found"));
>     }
>
>     @Transactional
>     public void updateUserEmail(Long id, String newEmail) {
>         User user = userRepository.findById(id).orElseThrow(() -> new RuntimeException("User not found"));
>         user.setEmail(newEmail);
>         userRepository.save(user);
>     }
>
>     @Transactional
>     public void performComplexOperation() {
>         // Example of a complex operation involving multiple steps
>         // Each step can be a separate method call, and all will be within the same transaction
>     }
> }
> ```


<!--ID:1706289784921-->
1. Spring REST annotations:
> **`@Controller`**: Indicates that a class serves the role of a controller in Spring MVC. It’s used to mark classes that handle HTTP requests.
> ```java
> @Controller
> public class MyController {
>     @RequestMapping("/")
>     public String home() {
>         return "home";
>     }
> }
> ```
>
> **`@RestController`**: convenience annotation that combines `@Controller` and `@ResponseBody`
> - JSON serialization if Jackson is on Classpath
> ```java
> @RestController
> public class MyRestController {
>     @GetMapping("/api/items")
>     public List<Item> getItems() {
>         return new ArrayList<>();
>     }
> }
> ```
>
> **`@RequestMapping`** (and its shortcuts like `@GetMapping`, `@PostMapping`): for mapping web requests onto methods in request handling classes.
> ```java
> @RestController
> public class MyController {
>     @RequestMapping(value = "/items", method = RequestMethod.GET)
>     public List<Item> getItems() {
>         return new ArrayList<>();
>     }
> }
> ```
>
> **`@PathVariable`**: Used in Spring MVC to bind a method parameter to a URI template variable.
> ```java
> @RestController
> public class MyController {
>     @GetMapping("/users/{id}")
>     public User getUser(@PathVariable Long id) {
>         // retrieve user by id
>     }
> }
> ```
>
> **`@RequestBody`**: Used to bind the HTTP request body to a method parameter in a controller, often for RESTful services.
> ```java
> @RestController
> public class MyController {
>     @PostMapping("/users")
>     public User createUser(@RequestBody User user) {
>         // create user
>     }
> }
> ```
>
> **`@RequestParam`**: **Explanation**: Binds a method parameter to a web request parameter.
> ```java
> @RestController
> public class MyController {
>     @GetMapping("/users")
>     public List<User> getUsers(@RequestParam String role) {
>         // find users by role
>     }
> }
> ```

---

# Operations .......................................................................................
```bash
java -jar target/myapplication-0.0.1-SNAPSHOT.jar

export JAVA_OPTS=-Xmx1024m
gradle bootRun
```

## DevTools
[Property Defaults for Dev](https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.devtools.property-defaults)
- automatic restart: trigger is to update the classpath



# Debugging ........................................................................................
find out what auto-configuration is currently being applied, and why, start your application with the --debug switch. Doing so enables debug logs for a selection of core loggers and logs a conditions report to the console.

```bash
java -jar myproject-0.0.1-SNAPSHOT.jar --debug

# Attach Debugger
java -Xdebug -Xrunjdwp:server=y,transport=dt_socket,address=8000,suspend=n -jar target/myapplication-0.0.1-SNAPSHOT.jar

# Flight Recorder (Startup tracking)
$ java -XX:StartFlightRecording:filename=recording.jfr,duration=10s -jar demo.jar
```

---
<!--ID:1706629777697-->
1. Find out why property has particular value:
> `env, configprops` Actuator endpoint

---
