val loaderoJavaVersion: String by project
val gsonVersion: String by project

plugins {
    java
    application
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}

application {
    mainClass.set("Main")
}

repositories {
    mavenCentral()
    maven(url = "https://jitpack.io")
}

dependencies {
    implementation("com.github.loadero:loadero-java:v$loaderoJavaVersion")
    implementation("com.google.code.gson:gson:$gsonVersion")
}
