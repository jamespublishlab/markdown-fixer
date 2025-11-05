plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "1.9.25"
    id("org.jetbrains.intellij.platform") version "2.10.4"
}

group = providers.gradleProperty("pluginGroup").get()
version = providers.gradleProperty("pluginVersion").get()

repositories {
    mavenCentral()

    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        create(providers.gradleProperty("platformType"), providers.gradleProperty("platformVersion"))

        // Add bundled Markdown plugin
        bundledPlugin("org.intellij.plugins.markdown")

        // Plugin Verifier
        pluginVerifier()

        // Test Framework
        testFramework(org.jetbrains.intellij.platform.gradle.TestFrameworkType.Platform)
    }

    // Unicode width calculation for table formatting
    implementation("com.ibm.icu:icu4j:74.2")

    testImplementation("junit:junit:4.13.2")
}

intellijPlatform {
    pluginConfiguration {
        name = providers.gradleProperty("pluginName")
        version = providers.gradleProperty("pluginVersion")

        ideaVersion {
            sinceBuild = providers.gradleProperty("pluginSinceBuild")
            untilBuild = providers.gradleProperty("pluginUntilBuild")
        }

        description = """
            Fixes common markdown formatting issues automatically.

            Features:
            - Adds proper blank lines around lists
            - Converts consecutive field-style metadata to bulleted lists
            - Collapses excessive newlines
            - Preserves code blocks and blockquotes
            - Formats markdown tables with proper alignment and column widths
            - Supports Unicode, CJK characters, and emoji in tables
        """.trimIndent()

        changeNotes = """
            <h2>1.0.0</h2>
            <ul>
                <li>Initial release</li>
                <li>Core markdown formatting functionality</li>
                <li>Right-click action for markdown files</li>
                <li>Table formatting with automatic column width calculation</li>
                <li>Unicode, CJK, and emoji support in tables</li>
            </ul>
        """.trimIndent()
    }

    publishing {
        token = providers.environmentVariable("PUBLISH_TOKEN")
    }

    signing {
        certificateChain = providers.environmentVariable("CERTIFICATE_CHAIN")
        privateKey = providers.environmentVariable("PRIVATE_KEY")
        password = providers.environmentVariable("PRIVATE_KEY_PASSWORD")
    }
}

tasks {
    withType<JavaCompile> {
        sourceCompatibility = "17"
        targetCompatibility = "17"
    }

    withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
        kotlinOptions.jvmTarget = "17"
    }

    test {
        useJUnit()
    }
}
