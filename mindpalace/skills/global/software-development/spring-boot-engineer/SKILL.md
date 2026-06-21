---
name: spring-boot-engineer
description: "Use when building Spring Boot 3.x apps, microservices, or reactive Java — REST controllers, Spring Security 6 auth, Spring Data JPA repositories, WebFlux endpoints, Spring Cloud. Triggers: Spring Boot, Spring Framework, Spring Cloud, Spring Security, Spring Data JPA, Spring WebFlux, Microservices Java, Java REST API, Reactive Java."
version: 1.0.0
license: MIT
tags: [spring-boot, java, spring-security, spring-data-jpa, webflux, spring-cloud, microservices, rest]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/spring-boot-engineer
derived_from: awesomeclaude
---

# Spring Boot Engineer

Spring Boot 3.x: REST, security, data, reactive, microservices.

## When to use

Spring Boot 3.x apps + microservices; REST controllers; Spring Security 6 auth flows; Spring Data JPA repositories; reactive WebFlux endpoints; Spring Cloud integration.

## Core workflow

1. **Analyze** — module structure, starters, config.
2. **Design** — entities, DTOs, repository interfaces.
3. **Implement** — `@RestController` → `@Service` → `@Repository`; constructor injection.
4. **Secure** — `SecurityFilterChain` bean, JWT/OAuth2.
5. **Test** — `@SpringBootTest`, `@DataJpaTest`, MockMvc/WebTestClient.

## Key practices

- Constructor injection (no field `@Autowired`); `@Service` for logic.
- Spring Data JPA: derived queries + `@EntityGraph`/fetch joins to avoid N+1.
- DTOs at the API boundary; never expose entities directly.
- Spring Security 6: lambda DSL `SecurityFilterChain`; stateless JWT for APIs.
- WebFlux: `Mono`/`Flux`, never block reactive threads.
- Externalized config via `application.yml` + profiles; secrets via env/Vault.

## Constraints

MUST: constructor injection; `@Transactional` at service layer; DTOs at boundary; correct filter-chain config; avoid N+1 (entity graphs/fetch joins); integration tests (Testcontainers).
MUST NOT: field injection; expose JPA entities in responses; block reactive chains; secrets in source; ignore N+1; mix blocking JDBC into WebFlux.

## Output

1. Entities + DTOs + repositories. 2. Controllers + services. 3. Security config. 4. Tests. 5. Brief note on data/security decisions.

## Knowledge

Spring Boot 3.x, Spring Framework, Spring Security 6, Spring Data JPA, WebFlux/Reactor, Spring Cloud, OAuth2/JWT, Hibernate, Maven/Gradle, Testcontainers, JUnit 5, MockMvc.
