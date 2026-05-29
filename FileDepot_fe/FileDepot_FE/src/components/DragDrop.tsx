import React from 'react'
import { FileUploader } from "react-drag-drop-files";
import { useEffect, useState } from "react";
import { Box, Text, Button, Flex } from "@chakra-ui/react";

interface Props {
    file: Blob,
    handleChange: (file) => void,
    handleSubmit: (file) => void,
    handleEmpty: () => void
}
const DragDrop = ({ file, handleChange, handleSubmit, handleEmpty }: Props) => {

    const fileTypes = ["TXT", "PDF"];

    return (
        <>
            <Box display="flex" flexDirection="column" alignItems="center" textAlign="center" color="teal">
                <Text mt={4} mb={4}>
                    Déposez (ou faites glisser) un fichier.
                </Text>
                <FileUploader handleChange={handleChange} name="file" label="Chargez ou déposez un fichier ici" uploadedLabel="Fichier chargé avec succès." hoverTitle="Déposer ici" types={fileTypes} />
                <Flex justify="space-between" align="stretch" gap={5} mt={4}>
                    {file &&
                        <>
                            <Button colorPalette="red" onClick={handleEmpty}>Vider</Button>
                            <Button onClick={handleSubmit}>Déposer</Button>
                        </>
                    }
                </Flex>
            </Box>
        </>
    )
}

export default DragDrop