package com.markdownfixer.actions

import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.intellij.openapi.command.WriteCommandAction
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.markdownfixer.MarkdownFixer

/**
 * Action to fix markdown formatting issues in the current file.
 *
 * This action appears in the context menu (right-click) for markdown files
 * in both the Project View and Editor.
 */
class FixMarkdownAction : AnAction() {

    private val logger = Logger.getInstance(FixMarkdownAction::class.java)
    private val fixer = MarkdownFixer()

    /**
     * Update the action's visibility and enabled state.
     * Only show and enable for markdown files.
     */
    override fun update(event: AnActionEvent) {
        // Try to get file from multiple sources (order matters!)
        var file = event.getData(CommonDataKeys.VIRTUAL_FILE_ARRAY)?.firstOrNull()
            ?: event.getData(CommonDataKeys.VIRTUAL_FILE)
            ?: event.getData(CommonDataKeys.PSI_FILE)?.virtualFile

        // If still null, try getting from navigatable array (Project View uses this!)
        if (file == null) {
            val navigatables = event.getData(CommonDataKeys.NAVIGATABLE_ARRAY)
            if (navigatables != null && navigatables.isNotEmpty()) {
                val firstNav = navigatables[0]

                // Try to extract VirtualFile from the navigatable
                when (firstNav) {
                    is com.intellij.psi.PsiFile -> {
                        file = firstNav.virtualFile
                    }
                    is com.intellij.openapi.fileEditor.OpenFileDescriptor -> {
                        file = firstNav.file
                    }
                    else -> {
                        // Try reflection to get virtualFile or file property
                        // This handles PsiFileNode and other wrapper types
                        try {
                            val virtualFileMethod = firstNav.javaClass.getMethod("getVirtualFile")
                            file = virtualFileMethod.invoke(firstNav) as? com.intellij.openapi.vfs.VirtualFile
                        } catch (e: Exception) {
                            try {
                                val fileMethod = firstNav.javaClass.getMethod("getFile")
                                file = fileMethod.invoke(firstNav) as? com.intellij.openapi.vfs.VirtualFile
                            } catch (e2: Exception) {
                                // Could not extract VirtualFile from navigatable
                                logger.debug("Could not extract VirtualFile from ${firstNav.javaClass.name}")
                            }
                        }
                    }
                }
            }
        }

        // Last resort: try single navigatable
        if (file == null) {
            val navigatable = event.getData(CommonDataKeys.NAVIGATABLE)
            if (navigatable is com.intellij.psi.PsiFile) {
                file = navigatable.virtualFile
            } else if (navigatable is com.intellij.openapi.fileEditor.OpenFileDescriptor) {
                file = navigatable.file
            }
        }

        val isMarkdown = file != null &&
            !file.isDirectory &&
            (file.extension == "md" || file.extension == "markdown")

        event.presentation.isEnabledAndVisible = isMarkdown
    }

    /**
     * Perform the action: fix markdown formatting in the current file.
     */
    override fun actionPerformed(event: AnActionEvent) {
        val project = event.project
        if (project == null) {
            logger.warn("No project found in action event")
            return
        }

        val file = event.getData(CommonDataKeys.VIRTUAL_FILE)
            ?: event.getData(CommonDataKeys.VIRTUAL_FILE_ARRAY)?.firstOrNull()

        if (file == null) {
            logger.warn("No file found in action event")
            showNotification(project, "Error", "No file selected", NotificationType.ERROR)
            return
        }

        try {
            // Get the document
            val document = FileDocumentManager.getInstance().getDocument(file)
            if (document == null) {
                logger.warn("Cannot get document for file: ${file.path}")
                showNotification(project, "Error", "Cannot read file", NotificationType.ERROR)
                return
            }

            // Get original content
            val originalContent = document.text

            // Process the content
            val fixedContent = fixer.fixString(originalContent)

            // Check if content actually changed
            if (originalContent == fixedContent) {
                showNotification(
                    project,
                    "No Changes",
                    "File is already properly formatted",
                    NotificationType.INFORMATION
                )
                return
            }

            // Write changes
            WriteCommandAction.runWriteCommandAction(project) {
                document.setText(fixedContent)
            }

            // Save document
            FileDocumentManager.getInstance().saveDocument(document)

            // Show success notification
            showNotification(
                project,
                "Markdown Fixed",
                "Successfully fixed markdown formatting in ${file.name}",
                NotificationType.INFORMATION
            )

            logger.info("Fixed markdown formatting in: ${file.path}")

        } catch (e: Exception) {
            logger.error("Failed to fix markdown formatting", e)
            showNotification(
                project,
                "Error",
                "Failed to fix markdown: ${e.message}",
                NotificationType.ERROR
            )
        }
    }

    /**
     * Show a notification to the user.
     */
    private fun showNotification(
        project: com.intellij.openapi.project.Project,
        title: String,
        content: String,
        type: NotificationType
    ) {
        NotificationGroupManager.getInstance()
            .getNotificationGroup("MarkdownFixer.Notifications")
            .createNotification(title, content, type)
            .notify(project)
    }
}
